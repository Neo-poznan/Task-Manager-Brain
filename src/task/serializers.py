import json
from typing import Any


def to_json(some_dictionary: dict[Any, Any]) -> json:
    return json.dumps(some_dictionary)


def from_json(some_json: json) -> dict[Any, Any]:
    return json.loads(some_json)

