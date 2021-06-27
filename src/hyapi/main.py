"""
Author: Preocts <Preocts#8196>
"""
import json
from typing import Any
from typing import Dict

import urllib3
from secretbox.loadenv import LoadEnv

secrets = LoadEnv(auto_load=True)


def player_loopup(uuid: str) -> Dict[str, Any]:
    """Super powerful docstring"""

    conn = urllib3.PoolManager()

    headers = {"Accept": "application/json"}
    fields = {"uuid": uuid, "key": secrets.get("HYAPI_APIKEY")}

    result = conn.request(
        "GET",
        "https://api.hypixel.net/player",
        fields=fields,
        headers=headers,
    )

    return json.loads(result.data.decode())


result = player_loopup("0a89731c-c40b-4c93-801f-96aa35bdf018")

open("out.json", "w").write(json.dumps(result["player"], indent=4))

print(len(result["player"]))
