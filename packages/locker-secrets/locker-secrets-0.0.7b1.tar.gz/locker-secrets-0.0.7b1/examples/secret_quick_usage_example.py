import os
from dotenv import load_dotenv

import locker
from locker.error import APIError

load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key


# Get list secrets
# secrets = locker.list()
# for secret in secrets:
#     print(secret.key, secret.value, secret.description, secret.environment_name)


# # Get a secret value by secret key. If the Key does not exist, the SDK will return the default_value
# secret_value = locker.get_secret("Key 1", default_value="TheDefaultValue")
# print(secret_value)
#
#
# # Update a secret value by secret key
# secret = locker.modify(key="Key 1", value="NEW_VAL_1", environment_name="Staging")
# print(secret.key, secret.value, secret.description, secret.environment_name)
#
#
# Create new secret
# new_secret = locker.create(key="GOOGLE_API", value="test")
# print(new_secret.key, new_secret.value, new_secret.description, new_secret.environment_name)

locker.log = "debug"
try:
    new_secret = locker.create(key="REDIS_CONNECTION", value="redis_connect_staging_2", environment_name="staging")
    print(new_secret.key, new_secret.value, new_secret.description, new_secret.environment_name)
except APIError as e:
    print(e.user_message)
    print(e.http_status)
    print(e.http_body)
    print(e.json_body)

# # Get a secret value by secret key. If the Key does not exist, the SDK will return the default_value
# secret_value = locker.get_secret("REDIS_CONNECTION", default_value="TheDefaultValue", environment_name="staging")
# print(secret_value)

# locker.log = 'debug'
# # locker.api_base = "http://127.0.0.1:9000"
# # Update a secret value by secret key
# secret = locker.modify(key="REDIS_CONNECTION", environment_name="staging", value="redis_connect_staginggg")
# print(secret.key, secret.value, secret.description, secret.environment_name)


# print("---")
# secrets = locker.list()
# for secret in secrets:
#     print(secret.key, secret.value, secret.description, secret.environment_name)
