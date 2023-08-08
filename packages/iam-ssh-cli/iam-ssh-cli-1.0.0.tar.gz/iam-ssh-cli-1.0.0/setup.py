#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


install_requires = [
    'boto3'
]


setup_options = dict(
    name='iam-ssh-cli',
    version='1.0.0',
    description='sync IAM ssh keys to Linux boxes.',
    long_description=read('README.rst'),
    author='Chathuranga Abeyrathna',
    author_email='chaturanga50@gmail.com',
    url='https://github.com/chaturanga50/iam-ssh-cli',
    scripts=['bin/iam-ssh-cli'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={},
    license="Apache License 2.0",
    python_requires=">= 3.7",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/chaturanga50/iam-ssh-cli/issues',
        'Source': 'https://github.com/chaturanga50/iam-ssh-cli',
        'Changelog': 'https://github.com/chaturanga50/iam-ssh-cli/blob/develop/CHANGELOG.rst',
    }
)

setup(**setup_options)
