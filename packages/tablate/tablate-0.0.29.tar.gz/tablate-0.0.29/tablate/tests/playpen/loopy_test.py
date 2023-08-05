import time

start_1 = time.perf_counter_ns()
for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass


for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

for i in range(0, 10):
    some_dict = {
        "one": "one",
        "two": "two",
        "three": "three"
    }

    if "dog" in some_dict:
        pass

end_1 = time.perf_counter_ns()

calc_1_ns = end_1 - start_1
calc_1_ms = calc_1_ns / 1000000
calc_1_s = calc_1_ms / 1000

print(f"{calc_1_ns} ns, {calc_1_ms} ms, {calc_1_s} s")

"""
SET ONE: 1 000 000

# 1

no load

34757386 ns, 34.757386 ms, 0.034757385999999994 s
31227723 ns, 31.227723 ms, 0.031227723000000002 s
29034961 ns, 29.034961 ms, 0.029034960999999998 s

# 2

declare dict

111380634 ns, 111.380634 ms, 0.111380634 s
118363397 ns, 118.363397 ms, 0.11836339700000001 s
126894729 ns, 126.894729 ms, 0.126894729 s

#3

add keys

166996227 ns, 166.996227 ms, 0.166996227 s
182324513 ns, 182.324513 ms, 0.182324513 s
173875968 ns, 173.875968 ms, 0.173875968 s

#4

if check, no load

161140329 ns, 161.140329 ms, 0.161140329 s
143606580 ns, 143.60658 ms, 0.14360658 s
144456696 ns, 144.456696 ms, 0.144456696 s
"""
