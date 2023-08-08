from __future__ import absolute_import, division, print_function

import json
import os
import stat
import sys
import subprocess
from six.moves.urllib.parse import urlencode

import locker
from locker import util, error
# from locker.error import CliRunError, AuthenticationError
from locker.logger import logger


class BinaryAdapter(object):
    def __init__(self, access_key=None, api_base=None, api_version=None):
        self.access_key = access_key
        self.api_base = api_base or locker.api_base
        self.api_version = api_version or locker.api_version
        self.system_platform = self.get_platform()

    @classmethod
    def make_executable(cls, path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    @staticmethod
    def get_platform():
        # Return darwin/win32/linux
        return sys.platform

    def get_binary_file(self):
        # Checking the os system, returns the corresponding binary
        # OS X
        if self.system_platform == "darwin":
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret_mac")
        # Windows
        elif self.system_platform == "win32":
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret.exe")
        # Default is linux
        else:
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret_linux")

    def call(
        self,
        cli,
        params=None,
        asjson=True,
        load=False,
        shell=True,
        timeout=30,
    ):
        binary_file = self.get_binary_file()
        if binary_file:
            self.make_executable(binary_file)
        if self.access_key:
            my_access_key = self.access_key
        else:
            from locker import access_key
            my_access_key = access_key
        if my_access_key is None:
            raise error.AuthenticationError(
                "No Access key provided. (HINT: set your API key using "
                '"locker.access_key = <ACCESS-KEY>"). You can generate Access Key '
                "from the Locker Secret web interface."
            )

        default_user_agent = f"Python{sys.version_info[0]}"
        command = f'{binary_file} {cli} --access-key "{my_access_key}" --api-base {self.api_base} ' \
                  f'--client {default_user_agent}'

        # Building full command with params
        post_data = None
        if "get" in cli or "delete" in cli:
            encoded_params = urlencode(list(util.api_encode(params or {})))
            # Don't use strict form encoding by changing the square bracket control
            # characters back to their literals. This is fine by the server, and
            # makes these parameter strings easier to read.
            encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")
            # TODO: Build api url by passing filter params to command
            # if params:
            #     abs_url = _build_api_url(abs_url, encoded_params)
            pass
        elif "update" in cli or "create" in cli:
            post_data = json.dumps(json.dumps(params or {}))
        if post_data:
            command += f' --data {post_data}'

        logger.debug(f"[+] Running cli command: {command}")
        try:
            raw = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT, shell=shell, universal_newlines=True, timeout=timeout
            )
            # if locker.skip_cli_lines > 0:
            #     raw = raw_result.split("\n", locker.skip_cli_lines)[locker.skip_cli_lines]
            # else:
            #     raw = raw_result
            # # Log break
            # try:
            #     raw = raw_result.split("----------- LOG BREAK -----------")[1]
            # except IndexError:
            #     pass
        except subprocess.TimeoutExpired as e:
            exc = error.CliRunError(e.stdout)
            exc.process = e
            raise exc
        except subprocess.CalledProcessError as e:
            signs = ['"success": false', '"success": true', '"object": "error"']
            if any(s in e.output for s in signs):
                raw = e.output
            elif str(e.output).strip() == 'Killed' or 'returned non-zero exit status 1' in str(e):
                exc = error.CliRunError(e.stdout)
                exc.process = e
                raise exc
            else:
                logger.warning(f"[!] subprocess.CalledProcessError: {e} {e.output}. The command is: {command}")
                exc = error.CliRunError(e.stdout)
                exc.process = e
                raise exc
        return self.interpret_response(res_body=raw, asjson=asjson)

    def interpret_response(self, res_body, asjson=True):
        # Skip cli lines
        if locker.skip_cli_lines > 0:
            res_body = res_body.split("\n", locker.skip_cli_lines)[locker.skip_cli_lines]
        # Log break
        try:
            res_body = res_body.split("----------- LOG BREAK -----------")[1]
        except IndexError:
            pass
        if not asjson:
            return res_body

        try:
            if hasattr(res_body, "decode"):
                res_body = res_body.decode("utf-8")
        except Exception:
            logger.error(f"[!] Invalid decode response body from CLI:::{res_body}")
            exc = error.CliRunError(
                f"Invalid decode response body from CLI: {res_body}",
                res_body
            )
            exc.process = res_body
            raise exc
        try:
            res_body = json.loads(res_body)
        except json.decoder.JSONDecodeError:
            logger.error(f"[!] CLI result json decode error:::{res_body}")
            exc = error.CliRunError(
                f"CLI JSONDecodeError:::{res_body}",
                res_body
            )
            exc.process = res_body
            raise exc
        res_body.update({"object": "error"})
        if self._should_handle_as_error(res_body):
            self.handle_error_response(res_body)
        return res_body

    @staticmethod
    def _should_handle_as_error(res_body):
        try:
            return res_body.get("object") == "error" or res_body.get("is_success") is False or \
                res_body.get("is_success") == "false"
        except AttributeError:
            return False

    def handle_error_response(self, res_body):
        exc = self.specific_cli_error(error_data=res_body)
        raise exc

    @staticmethod
    def specific_cli_error(error_data):
        logger.info(f"[!] CLI return error object:::{error_data}")
        status_code = error_data.get("status_code")
        error_code = error_data.get("error")
        if status_code == 429 or error_code == "rate_limit":
            return error.RateLimitError(
                error_data.get("message"), error_data
            )
        elif status_code == 401 or error_code == "unauthorized":
            return error.AuthenticationError(
                error_data.get("message"), error_data
            )
        elif status_code == 403 or error_code == "permission_denied":
            return error.PermissionDeniedError(
                error_data.get("message"), error_data
            )
        else:
            return error.APIError(
                error_data.get("message"), error_data
            )
