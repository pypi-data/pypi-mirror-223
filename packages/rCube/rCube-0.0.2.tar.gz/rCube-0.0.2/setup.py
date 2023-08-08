import setuptools


setuptools.setup(
    name = "rCube",
    version = "0.0.2",
    author = "seth",
    author_email = "imageseth@gmail.com",
    description = "Generalized puzzle cube framework",
    packages = setuptools.find_packages(where="rCube"),
    install_requires=[
          'numpy',
          'matplotlib'
      ],
    python_requires = ">=3.6"
)