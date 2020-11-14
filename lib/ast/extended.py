from dataclasses import dataclass
from . basic import BaseASTNode


@dataclass(eq=False)
class Drop(BaseASTNode):
    pass


@dataclass(eq=False)
class Add(BaseASTNode):
    shift: int


@dataclass(eq=False)
class Sub(BaseASTNode):
    shift: int


@dataclass(eq=False)
class Mul(BaseASTNode):
    #[->+++>+++++++<<]
    # mem[p+1] += mem[p] * 3;
    # mem[p+2] += mem[p] * 7;
    # mem[p] = 0
    shift0: int
    shift1: int
    mul0: int
    mul1: int
