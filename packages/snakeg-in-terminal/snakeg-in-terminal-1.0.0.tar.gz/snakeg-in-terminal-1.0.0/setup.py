from setuptools import find_packages, setup

VERSION = "1.0.0"
DESCRIPTION = "A snake-game like implementation"
LONG_DESCRIPTION = (
    'A package that allows the user to play the well known game calles "snake game"'
)

# Setting up
setup(
    name="snakeg-in-terminal",
    version=VERSION,
    author="crnvl96",
    author_email="<adran.carnavale@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pygame"],
    keywords=["python", "game", "pygame", "terminal", "snake"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
