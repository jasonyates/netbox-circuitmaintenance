#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    author="Jason Yates",
    author_email='me@jasonyates.co.uk',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="NetBox plugin for circuitmaintenance.",
    install_requires=requirements,
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='netbox_circuitmaintenance',
    name='netbox_circuitmaintenance',
    packages=find_packages(include=['netbox_circuitmaintenance', 'netbox_circuitmaintenance.*']),
    test_suite='tests',
    url='https://github.com/jasonyates/netbox-circuitmaintenance',
    version='0.2.1',
    zip_safe=False,
)
