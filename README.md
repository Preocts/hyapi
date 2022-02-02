# python-template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/hyapi/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/hyapi/main)
[![Python package](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/hyapi/actions/workflows/python-tests.yml)

# HyAPI

Hypixel API Wrapper - Early Development

Picked up for pattern exercises, not sure how far I'll take this.  All name lookups are Minecraft Java Edition accounts.

## Install via `pip`

*note: replace `vX.X.X` with desired library version. Installing from `main` can including breaking changes.*

```
python -m pip install git+https://github.com/Preocts/hyapi.git@vX.X.X
```

## Requirements
- [Python](https://python.org) >= 3.8
- [secretbox](https://pypi.org/project/secretbox) >= 2.3.3
- [urllib3](https://pypi.org/project/urllib3/) >= 1.26.8

---

## Internal Links

- [Development Installation Guide](docs/development.md)


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

The Player object represents the Hypixel data for a single target player. The `.fetch_player(player_id)` method will populate the object with Data, Friends, Status, Recent Games, and Guild information.  If the provided displayname or UUId is invalid/not found an empty object is returned.

The methods for accessing the information loosely follow the Hypixel public API: https://api.hypixel.net/#tag/Player-Data

- `Player.fetch_player(player_id: str)` : Pull all available information from the Hypixel API
  - `.data` : Various datapoints including displayname, rank, and stats
  - `.friends.records` : List of Friend objects containing UUIDs of who sent the friend request and who recieved it
  - `.status.session` : Current status information of the player
  - `.games.games` : List of Game objects containing the player's recently played games
  - `.guild` : If the player is in a guild the name and id is provided

All attributes have `.raw_data` available which contains a `Dict[str, Any]` of the response from Hypixel API

```py
from hyapi.player import Player

# Create Player instance
uuid = "[UUID or current display name here]"
player = Player()

# Load player by UUID or display name
player.fetch_player(uuid)

# Results will be empty if load fails
print(f"Display name: {player.data.displayname}")
print(f"Current guild: {player.guild.name}")
print(f"Number of friends: {len(player.friends.records)}")
print(f"Currently online: {player.status.session.online}")
print(f"Number of recent games: {len(player.games.games)}")
```
