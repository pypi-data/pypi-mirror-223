# Build Python package for installing different OS Platform VulcanSQL CLI Binary Executable file

The project focus on building the VulcanSQL binary files to the Python package to make user could install VulcanSQL by `pip install` in the Python.

If you would like to download the source code and develop new feature or fix bug, please follow the guide below to build development environment.

# Prerequisite

Before you start to develop, please make sure we prepared the python version we supported and [poetry](https://python-poetry.org/) package which the python package and dependency management tools.

## 1. Install Poetry

```sh
$> pip install poetry
$> poetry about

Poetry - Package Management for Python

Poetry is a dependency manager tracking local dependencies of your projects and libraries.
See https://github.com/python-poetry/poetry for more information.
```

## 2. Setup virtual environment and install packages by poetry

Using the poetry to build virtual environment and install the required package which `pyproject.toml` records.

```sh
$> cd python-package
python-package $> poetry install      # install development required packages, will update poetry.lock and create .venv directory
python-package $> poetry shell        # enter virtual environments
(.venv) python-package $>
```

# Something need to know before developing

## The binary files location

The vulcan-sql binary files download from remote public url location, please remember to change the binary files location and check the filename, our `cli.py` will recognize the OS system get pick the correct binary to use.

## Use `poetry` to manage development environment and use `setup.py` to set configuration for build `vulcan-sql` package

Although using the poetry to manage our development environment and lock the dependencies but not using poetry to build package and publish it, because using poetry to build package may not work on older Python versions.

Therefore, we use `setup.py` to build and publish package to make older Python could still work to install package, so when need to update build configuration, please update `setup.py`.

## Use `entry_points` to support `vulcan` command after installing `vulcan-sql` package

We defined the `vulcan` command in the `entry_points` of the `setup.py`, so that we could type the command `vulcan` after `pip install vulcan-sql`.

When user type `vulcan`, it will trigger to get correct zip binary file for correct OS system and extract to use directly.

## Use `MANIFEST.in` to add files into `vulcan-sql` package

If you need to add some files into the package when building, please update `MANAIFEST.in`.

We set the value `include_package_data` to true to make `setup.py` read the `MANAIFEST.in` to decide which files (non `.py` files) to put into our package when building it, the reason it that `package_data` and `data_files` options may has some issue to add files, please see the [issue discussion](https://github.com/pypa/sampleproject/issues/30).

## How to test package on different Python versions

Because supporting python versions from `3.4.x` to `3.11.x`, it not easy to manage multiple python versions and switch it to test `pip install vulcan-sql`.

Therefore, suggest to use the [pyenv](https://github.com/pyenv/pyenv) to test your Python package by using `pip install` on your local environment, please make sure you have switch to the version we supported.

# Build

Before starting to build, **remember to update `version` in the `setup.py` and `pyproject.toml`**.

```bash
# Removed old distribution
$> rm -rf dist
# Build source distribution (please follow the more detail about setuptools document)
$> python setup.py sdist
```

# Test to install local `vulcan-sql` package before publishing

Switch to the python version you would like to test and do the step:

```bash
$> pip install <related-location>/dist/vulcan-sql-x.x.x.tar.gz
```

# Build and Publish

After you finished the development and test would like to publish to remote repository like [pypi](https://pypi.org/project/canner-python-client/).

```sh
# Removed old distribution
$> rm -rf dist
# Build source distribution (please follow the more detail about setuptools document)
$> python setup.py sdist
# upload to pypi and type account & password
$>  twine upload dist/*
```
