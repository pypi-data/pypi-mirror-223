import os
from dotenv import load_dotenv

import locker


# Set up access key
load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key


# Get list environments
environments = locker.list_environments()
for environment in environments:
    print(environment.id, environment.name, environment.external_url, environment.description)


# Get an environment by name
environment = locker.get_environment("Staging")
print(environment.id, environment.name, environment.external_url, environment.description)


# Update an environment by name
environment = locker.modify_environment(name="Staging", external_url="staging.demo.environment")
print(environment.id, environment.name, environment.external_url, environment.description)


# Create new environment
new_environment = locker.create_environment(name="Production", external_url="prod.demo.environment")
print(new_environment.id, new_environment.name, new_environment.external_url, new_environment.description)
