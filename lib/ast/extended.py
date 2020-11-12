from dataclasses import dataclass
from . basic import BaseASTNode


@dataclass
class Drop(BaseASTNode):
    pass


@dataclass
class Add(BaseASTNode):
    shift: int
    def __init__(self, shift: int):
        self.shift = shift


@dataclass
class Sub(BaseASTNode):
    shift: int
    def __init__(self, shift: int):
        self.shift = shift

