"""
Testing the difference between JSON and Cain
"""

import json
import typing
from nasse.timer import Timer

from cain.types import Object, String
# from cain.types.characters import FIXED_CASE, UPPER_CASE

TEST = {
    "b": 3,
    "c": 5.5,
    "d": True,
    "e": {
        "f": False,
        # "g": b"Hello world"
        "h": "HELLO WORLD",
        "i": "Hi!",
        "j": [1, 2, 3],
        "k": (1, "hello", True),
        "l": None,
        "m": "Yay",
        "n": "Hi",
        "o": 2,
        "p": None
    }
}

# JSON Encode
print("JSON Encode")
print("-----------")

with Timer() as t:
    json_encoded = json.dumps(TEST, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
json_encode_time = t.time_ns
print(f"JSON encode time: {json_encode_time}ns")
print("JSON encode results:", json_encoded)

with Timer() as t:
    json_decoded = json.loads(json_encoded)
json_decoded_time = t.time_ns
print(f"JSON decode time: {json_decoded_time}ns")
print("JSON decode results:", json_decoded)
print("Original equality?", TEST == json_decoded)

print()
print("CAIN Encode")
print("-----------")


class ObjectA(Object):
    """test object A"""
    class ObjectB(Object):
        """test object B"""
        f: bool
        # g: bytes
        # h: String[FIXED_CASE, UPPER_CASE]
        h: str
        i: str
        j: list[int]
        k: tuple[int, str, bool]
        l: typing.Optional[str]
        m: typing.Optional[str]
        n: typing.Union[str, int]
        o: typing.Union[str, int]
        p: None

    b: int
    c: float
    d: bool
    e: ObjectB


a = ObjectA(TEST)

with Timer() as t:
    cain_encoded = a.encoded
cain_encode_time = t.time_ns
print(f"CAIN encode time: {cain_encode_time}ns ({round(((cain_encode_time / json_encode_time)) * 100, 2)}%)")
print("CAIN encode results:", cain_encoded)

with Timer() as t:
    cain_decoded = a.decode(cain_encoded)
cain_decoded_time = t.time_ns
print(f"CAIN decode time: {cain_decoded_time}ns ({round(((cain_decoded_time / json_decoded_time)) * 100, 2)}%)")
print("CAIN decode results:", cain_decoded)
print("Original equality?", TEST == cain_decoded)

print()
print("Comparisons")
print("-----------")

print(f"CAIN/JSON encode size ratio: {round(((len(cain_encoded) / len(json_encoded))) * 100, 2)}% of JSON Size")
print(f"CAIN/JSON encode size gains: {round((1 - (len(cain_encoded) / len(json_encoded))) * 100, 2)}% smaller")
print("CAIN/JSON decoding equality?", cain_decoded == json_decoded)

with open("test.json", "w+b") as f:
    f.write(json_encoded)

with open("test.cain", "w+b") as f:
    f.write(cain_encoded)
