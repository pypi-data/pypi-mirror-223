from dataclasses import dataclass
from typing import TypedDict, NamedTuple
from collections import namedtuple
import attr

from tablate.type.type_base import HtmlOuterBase
from tablate.type.type_input import HtmlOuterStylesInput


class SomeDictClass(TypedDict):
    field3: str

class SomeTuple(NamedTuple):
    field1: str = "bob"
    field2: int = 3

@dataclass
class SomeDataClass:
    field1: str = "bob"
    field2: int = 3


@dataclass
class SomeSubDataClass(SomeDataClass):
    field3: str = ""
    field4: int = 3


some_dataclass = SomeSubDataClass()


# SomeOtherTuple = namedtuple("SomeTuple", ("blah": int))


def some_func(arg1: str, arg2: int, arg3: SomeTuple):
    print(arg3)


some_func(arg1="some string",
          arg2=243,
          arg3=SomeTuple(field1="mary",
                         field2=4))


class SomeSubTuple(SomeTuple):
    field3: str = "bob"
    field4: int = 3

name_tup = SomeSubTuple()

HtmlOuterStylesInput()
HtmlOuterBase()
