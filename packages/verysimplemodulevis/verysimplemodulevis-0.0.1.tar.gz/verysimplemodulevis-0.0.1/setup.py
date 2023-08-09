from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Meu primeiro projeto em Python'
LONG_DESCRIPTION = 'Esta é a descrição longa do meu projeto.'

# Configurando o setup
setup(
    name="verysimplemodulevis",
    version=VERSION,
    author="Victor Macedo",
    author_email="victormacedocarvalho09@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Adicione "verysimplemodule" à lista de pacotes
    install_requires=[],

    # Outras informações relevantes
    keywords='python module example',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],    
)