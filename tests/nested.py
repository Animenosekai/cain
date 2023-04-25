import json

from nasse.timer import Timer

from cain.types import Object


class A(Object):
    yay: str


class B(Object):
    yay: A


class C(Object):
    yay: B


class D(Object):
    yay: C


class E(Object):
    yay: D


class F(Object):
    yay: E


class G(Object):
    yay: F


class H(Object):
    yay: G


class I(Object):
    yay: H


class J(Object):
    yay: I


class K(Object):
    yay: J


class L(Object):
    yay: K


class M(Object):
    yay: L


class N(Object):
    yay: M


class O(Object):
    yay: N


class P(Object):
    yay: O


class Q(Object):
    yay: P


class R(Object):
    yay: Q


class S(Object):
    yay: R


class T(Object):
    yay: S


class U(Object):
    yay: T


class V(Object):
    yay: U


class W(Object):
    yay: V


class X(Object):
    yay: W


class Y(Object):
    yay: X


class Z(Object):
    yay: Y


TEST = {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {
    'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': {'yay': 'Hey'}}}}}}}}}}}}}}}}}}}}}}}}}}

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

a = Z(TEST)

with Timer() as t:
    cain_encoded = a.encoded
cain_encode_time = t.time_ns
print(f"CAIN encode time: {cain_encode_time}ns ({round(((cain_encode_time / json_encode_time)) * 100, 2)}%)")
print("CAIN encode results:", cain_encoded)

with Timer() as t:
    cain_decoded = a.decoded(cain_encoded)
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
