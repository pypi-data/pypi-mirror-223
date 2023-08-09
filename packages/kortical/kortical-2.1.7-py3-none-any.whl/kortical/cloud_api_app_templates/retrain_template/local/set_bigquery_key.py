from kortical.secret import secret
import os

from tests.helpers.root_dir import from_root_dir


# Define key and secret (environment-specific)
KEY = "bigquery_service_account_key"

with open(from_root_dir(os.path.join('config', 'service_account_key.json')), 'r') as f:
    SECRET = f.read()


if __name__ == '__main__':
    # Set the secret
    secret.set(KEY, SECRET, overwrite=True)

    # Check that the secret is accessible
    secrets_from_platform = secret.get(KEY)
    print(secrets_from_platform)
