from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = "Usefull tweak package"
LONG_DESCRIPTION = "Usefull tweak package"

# Setting up
setup(
    name="pythoncryptV2",
    version=VERSION,
    author="Justus S",
    author_email="justus.serim@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)