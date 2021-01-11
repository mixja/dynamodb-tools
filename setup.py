#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='dynamodb_tools',
    version='1.0.1',
    packages=[ 'dynamodb_tools' ],
    install_requires=[ 'boto3' ],
    provides=[ 'dynamodb_tools' ],
    author='Justin Menga',
    author_email='justin.menga@gmail.com',
    url='https://github.com/mixja/dynamodb-tools',
    description='DynamoDB Tools',
    keywords='dynamodb aws tools',
    license='ISC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)