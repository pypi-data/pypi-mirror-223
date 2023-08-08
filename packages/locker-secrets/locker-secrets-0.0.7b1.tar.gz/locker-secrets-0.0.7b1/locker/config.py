import json
import pathlib


class Config:
    def __init__(self, config):
        if self._is_file_path(config):
            with open(config) as json_file:
                json_data = json.loads(json_file)
        elif isinstance(config, dict):
            json_data = config
        else:
            raise ValueError(
                'Invalid config argument: "{0}". Config argument must be a file path, '
                'or a dict containing the parsed file contents.'.format(config)
            )
        self.json_config = json_data

    @staticmethod
    def _is_file_path(path):
        try:
            pathlib.Path(path)
            return True
        except TypeError:
            return False

    @property
    def access_token(self):
        return self.json_config.get("access_token")

    @property
    def binary_path(self):
        return self.json_config.get("binary_path")

    @property
    def binary_config_path(self):
        return self.json_config.get("binary_config_path")
