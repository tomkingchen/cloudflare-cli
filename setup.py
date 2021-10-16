from setuptools import setup

setup(
    name='flare',
    version='0.1.0',
    author='Tom Chen',
    description='Cloudflare cli tool talks directly to Cloudflare API, so you dont have to.',
    py_modules=['flare'],
    install_requires=[
        'boto3',
        'botocore',
        'click',
        'pyyaml',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'flare = flare:cli',
        ],
    },
)