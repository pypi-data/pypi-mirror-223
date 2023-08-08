import setuptools


setuptools.setup(
    name = "rCube",
    version = "0.0.1",
    author = "philc",
    author_email = "imageseth@gmail.com",
    description = "Generalized puzzle cube framework",
    packages = setuptools.find_packages(where="rCube"),
    python_requires = ">=3.6"
)