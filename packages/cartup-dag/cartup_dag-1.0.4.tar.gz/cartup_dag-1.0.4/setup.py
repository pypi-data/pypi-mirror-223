from setuptools import setup, find_packages
from io import open
import sys

with open('docs/README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cartup_dag',
    version='1.0.4',
    license='Apache',
    description='DAG Job Library.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='arvind@cartup.ai',
    author='Arvind Rapaka',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
