import inspect
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int = 1  # Set default value

def f(a:str, b: int, c: bool = True):
    pass

func_sigs = inspect.getfullargspec(f)

print(func_sigs)

def some_func(arg: str = None):
    print(arg)


