import os
from dotenv import load_dotenv

load_dotenv()


def load_env_value(key):
    if os.getenv(key) is None:
        with open('.env', 'a') as f:
            value = input(f'Enter the value for {key}: ')
            f.write(f'{key}={value}\n')
            return value
    else:
        return os.getenv(key)
