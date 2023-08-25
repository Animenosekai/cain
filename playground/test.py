"""
Testing features on Cain
"""

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
        "g": b"Hello world",
        "h": "Hello 世界",
        "i": "Hi!",
        "j": [1, 2, 3],
        "k": {1, 2, 3},
        "l": (1, "hello", True),
        "m": None,
        "n": "Yay",
        "o": "Hi",
        "p": 2,
        "q": None,
        "r": range(1, 10, 2)
    }
}

print("CAIN Encode")
print("-----------")


class ObjectA(Object):
    """test object A"""
    class ObjectB(Object):
        """test object B"""
        f: bool
        g: bytes
        # h: String[FIXED_CASE, UPPER_CASE]
        h: String
        i: str
        j: list[int]
        k: typing.Set[int]
        l: tuple[int, str, bool]
        m: typing.Optional[str]
        n: typing.Optional[str]
        o: typing.Union[str, int]
        p: typing.Union[str, int]
        q: None
        r: range

    b: int
    c: float
    d: bool
    e: ObjectB


a = ObjectA(TEST)

with Timer() as t:
    cain_encoded = a.encoded
cain_encode_time = t.time_ns
print(f"CAIN encode time: {cain_encode_time}ns")
print("CAIN encode results:", cain_encoded)

with Timer() as t:
    cain_decoded = a.decoded(cain_encoded)
cain_decoded_time = t.time_ns
print(f"CAIN decode time: {cain_decoded_time}ns")
print("CAIN decode results:", cain_decoded)

print("Original equality?", TEST == cain_decoded)

with open("test.cain", "w+b") as f:
    f.write(cain_encoded)
