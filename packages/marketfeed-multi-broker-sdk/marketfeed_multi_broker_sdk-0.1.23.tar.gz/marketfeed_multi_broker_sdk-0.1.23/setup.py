from setuptools import setup, find_packages
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='marketfeed_multi_broker_sdk',
    version='0.1.23',
    url='https://github.com/tradeclone/multi-broker-sdk',
    author='Faraz',
    author_email='faraz.s@marketfeed.com',
    description='Multi Broker SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
        'pyotp',
        'load_dotenv'
    ],
)
