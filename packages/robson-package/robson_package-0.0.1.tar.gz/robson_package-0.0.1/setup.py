from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Meu primeiro pacote em Python'
LONG_DESCRIPTION = 'Meu primeiro pacote em Python com uma descrição im pouco mais longa'

# Setting up
setup(
    name="robson_package",
    version=VERSION,
    author="Robson-tech",
    author_email="robson.junior@ufpi.edu.br",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
)