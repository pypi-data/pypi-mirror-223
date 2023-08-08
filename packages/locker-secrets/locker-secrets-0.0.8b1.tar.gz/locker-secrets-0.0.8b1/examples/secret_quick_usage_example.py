import os
from dotenv import load_dotenv

import locker
from locker.error import APIError


load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key
locker.log = 'debug'


# Get list secrets
secrets = locker.list()
for secret in secrets:
    print(secret.key, secret.value, secret.description, secret.environment_name)


# Get a secret value by secret key. If the Key does not exist, the SDK will return the default_value
secret_value = locker.get_secret("REDIS_CONNECTION", default_value="TheDefaultValue")
print(secret_value)


# Get a secret value by secret key and specific environment name.
# If the Key does not exist, the SDK will return the default_value
secret_value = locker.get_secret("REDIS_CONNECTION", environment_name="staging", default_value="TheDefaultValue")
print(secret_value)


# Update a secret value by secret key
secret = locker.modify(key="GOOGLE_API_KEY",  value="new_google_api_key_value")
print(secret.key, secret.value, secret.description, secret.environment_name)

# Update a secret value by secret key and a specific environment name
secret = locker.modify(key="REDIS_CONNECTION",  environment_name="staging", value="staging.redis.connection")
print(secret.key, secret.value, secret.description, secret.environment_name)


# Create new secret and handle error
try:
    new_secret = locker.create(key="MYSQL_CONNECTION", value="mysql_connection_staging", environment_name="staging")
    print(new_secret.key, new_secret.value, new_secret.description, new_secret.environment_name)
except APIError as e:
    print(e.user_message)
    print(e.http_body)
