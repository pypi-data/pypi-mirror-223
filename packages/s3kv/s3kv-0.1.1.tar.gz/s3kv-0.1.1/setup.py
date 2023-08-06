from setuptools import setup

setup(
    name='s3kv',
    version='0.1.1',
    author='Balaji Bal',
    description='A Python library for interacting with S3 key-value store',
    long_description='A Python library for interacting with S3 key-value store',
    long_description_content_type='text/plain',
    url='https://github.com/BalLab/s3kv',
    packages=['s3kv'],
    install_requires=[
        'boto3', 'elasticsearch'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)