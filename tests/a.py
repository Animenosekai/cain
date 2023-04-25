import string

results = []

results.append("from cain.types import Object")
results.append("")

results.append("class A(Object):")
results.append("    yay: str")
results.append("")

for index, letter in enumerate(string.ascii_uppercase[1:]):
    results.append(f"class {letter}(Object):")
    results.append(f"    yay: {string.ascii_uppercase[index]}")
    results.append("")


def create(remaining):
    if not remaining:
        return "'Hey'"
    return f"{{'yay': {create(remaining[1:])}}}"


results.append(f"TEST = {create(string.ascii_uppercase)}")

with open("nested.py", "w") as f:
    f.write("\n".join(results))
