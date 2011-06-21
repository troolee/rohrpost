#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

try:
    license = open('LICENSE').read()
except:
    license = None

try:
    readme = open('README').read()
except:
    readme = None

setup(
    name='Rohrpost',
    version='0.0.1',
    author='Pavel Reznikov',
    author_email='pashka.reznikov@gmail.com',
    packages=['rohrpost'],
    scripts=[],
    url='https://github.com/troolee/rohrpost',
    license=license,
    description='',
    long_description=readme,
    requires=['tornadio'],
    install_requires=[
        'tornado >= 0.0.4'
    ]
)
