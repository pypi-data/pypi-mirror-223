from setuptools import setup

VERSION = '0.0.26'
DESCRIPTION = 'Meu primeiro pacote em Python'
LONG_DESCRIPTION = 'Meu primeiro pacote em Python com uma descrição um pouco mais longa'

# Setting up
setup(
    name="robson_package",
    version=VERSION,
    author="Robson-tech",
    author_email="robson.junior@ufpi.edu.br",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["robson_package"],
    install_requires=[],
)