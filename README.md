# python-template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/hyapi/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/hyapi/main)
[![Python package](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml)

# HyAPI

Hypixel API Wrapper - Early Development

Picked up for pattern exercises, not sure how far I'll take this.  All name lookups are Minecraft Java Edition accounts.

### Requirements
- [Python](https://python.org) >= 3.9
- [secretbox](https://pypi.org/project/secretbox) >= 1.1.0
- [urllib3](https://pypi.org/project/urllib3/) >= 1.26.6

---

Install instructions: To be created

```
pip install git+https://github.com/Preocts/hyapi.git
```

---

## Mojang API

Uses Mojang's public API to resolve player account data

### UUIDLookup

```py
from hyapi.uuidlookup import UUIDLookup

lookup_client = UUIDLookup()

# Resolve player from UUID
player = lookup_client.resolve_by_uuid("[UUID]")

# Resolve player from displayname (current)
player = lookup_client.reslove_by_name("[DisplayName]")

# Will have values if valid, will be empty strings if not
print(player.id)
print(player.uuid)
```


---

## Hypixel API

Uses Hypixel's public API to pull player data. Requires an API key.

### `.env`

Create a .env file in the root directory of your project. In it add the following line with the API key from Hypixel. To get an API key you must log into the Hypixel servers (in game) and type `/api` in the game chat.

```
HYAPI_APIKEY=[API KEY]
```

Alternative: Set an environment variable of the same name

### Player

```py
from hyapi.player import Player

# Create Player instance
player = Player()

# Load player by UUID or display name
player.load("[UUID or dispaly name]")

# Results will be empty if load fails
print(player.read.displayname)

# Raw JSON response from Hypixel can be accessed
print(player.read.raw_data)
```

---

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
