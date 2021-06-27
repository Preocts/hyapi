# python-template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/hyapi/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/hyapi/main)
[![Python package](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml)

# HyAPI

Hypixel API Wrapper

### Requirements
- Python >= 3.9

## Local developer installation

It is **highly** recommended to use a `venv` for installation. Leveraging a `venv` will ensure the installed dependency files will not impact other python projects or system level requirements.

The instruction below make use of a bash shell and a Makefile.  All commands should be able to be run individually of your shell does not support `make`

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/Preocts/[MODULE_NAME]
$ cd [MODULE_NAME]
```

Create and activate `venv`:
```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

Your command prompt should now have a `(venv)` prefix on it.

Install editable library and development requirements:
```bash
(venv) $ pip install -r requirements-dev.txt
(venv) $ pip install --editable .
```

Install pre-commit hooks to local repo:
```bash
(venv) $ pre-commit install
```

Run tests
```bash
(venv) $ tox
```

To exit the `venv`:
```bash
(venv) $ deactivate
```

---

### Makefile

This repo has a Makefile with some quality of life scripts if your system supports `make`.

- `update` : Clean all artifacts, update pip, update requirements, install everything
- `clean-pyc` : Deletes python/mypy artifacts
- `clean-tests` : Deletes tox, coverage, and pytest artifacts
- `build-dist` : Build source distribution and wheel distribution
