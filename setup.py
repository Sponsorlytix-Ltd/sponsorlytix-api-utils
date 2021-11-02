from setuptools import find_packages, setup

requirements = [
    'boto3',
    'botocore',
    'jmespath',
    'pymongo',
    'python-dateutil',
    's3transfer',
    'selenium',
    'six',
    'urllib3'
]

setup(
    name='sponsorlytix_api_utils',
    description='Sponsorlytix code utils',
    version='1.2',
    author='Sponsorlytix Team',
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
