"""
Setup.py for the param_persist library.
"""
from os import path

from setuptools import find_namespace_packages, setup

app_package = 'param_persist'
release_package = app_package

requirements = [
    'sqlalchemy',
]

test_requirements = [
    'pytest==5.4.1'
]

setup_directory = path.abspath(path.dirname(__file__))
with open(path.join(setup_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=release_package,
    version='0.0.8',
    description='The param_persist provides functionality to persist param classes.',
    long_description=long_description,
    author='gagelarsen',
    author_email='glarsen@aquaveo.com',
    url='https://github.com/Aquaveo/param_persist',
    license='BSD 2-Clause License',
    packages=find_namespace_packages(),
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
)
