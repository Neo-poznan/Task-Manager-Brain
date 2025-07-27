import json
from typing import Any


def to_json(some_dictionary: dict[Any, Any]) -> json:
    return json.dumps(some_dictionary)

