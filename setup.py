from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cinema21',
    version='1.0.0',
    description='A simple Cinema21 API wrapper.',
    long_description=long_description,
    url='https://github.com/cwkfr/cinema21-py',
    author='CWKFR',
    author_email='cwkfr@protonmail.com',
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cinema21 unofficial api',
    py_modules=["cinema21"],
    install_requires=['requests'],
    project_urls={
        'Bug Reports': 'https://github.com/cwkfr/cinema21-py/issues',
    },
)
