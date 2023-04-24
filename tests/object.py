from cain.types import Object


class ObjectA(Object):
    a: str
    b: int


a = ObjectA(a="hello", b=1)
print(a.copy)
print(a.copy())
