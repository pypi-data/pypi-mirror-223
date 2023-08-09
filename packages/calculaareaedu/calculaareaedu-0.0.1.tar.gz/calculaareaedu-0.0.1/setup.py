from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'meu primeiro pacote'
LONG_DESCRIPTION = 'descricao detalhada'

# Setting up
setup(
    name="calculaareaedu",
    version=VERSION,
    author="Luis Eduardo",
    author_email="le1307114@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python','first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
