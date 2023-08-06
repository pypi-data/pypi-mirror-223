"""
Quart-Kroket
-------------
zZzZ
"""
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


INSTALL_REQUIRES = open("requirements.txt").read().splitlines()

setup(
    name='Quart-Kroket',
    version='1.0.7',
    url='https://git.kroket.io/labs/quart-kroket',
    author='Kroket Ltd.',
    author_email='code@kroket.io',
    description='zZzZ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['quart_kroket'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    tests_require=INSTALL_REQUIRES + ["asynctest", "hypothesis", "pytest", "pytest-asyncio"],
    extras_require={"dotenv": ["python-dotenv"]},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
