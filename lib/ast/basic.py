from typing import List
from dataclasses import dataclass


@dataclass
class BaseASTNode:

    def to_bf_code(self) -> str:
        raise NotImplementedError()


@dataclass(eq=False)
class SimpleInstruction(BaseASTNode):
    repeat: int

    def __eq__(self, other: BaseASTNode) -> bool:
        return type(self) is type(other) and self.repeat == other.repeat # type: ignore

    def to_bf_code(self) -> str:
        return self.bf_instruction * self.repeat # type: ignore


@dataclass(eq=False)
class Inc(SimpleInstruction):
    bf_instruction = '+'


@dataclass(eq=False)
class Dec(SimpleInstruction):
    bf_instruction = '-'


@dataclass(eq=False)
class Right(SimpleInstruction):
    bf_instruction = '>'


@dataclass(eq=False)
class Left(SimpleInstruction):
    bf_instruction = '<'


@dataclass(eq=False)
class Input(SimpleInstruction):
    bf_instruction = ','


@dataclass(eq=False)
class Output(SimpleInstruction):
    bf_instruction = '.'


@dataclass(eq=False)
class Loop(BaseASTNode):
    contains: List[BaseASTNode]

    def to_bf_code(self) -> str:
        return '[%s]' % ''.join(node.to_bf_code() for node in self.contains)  #type: ignore


@dataclass(eq=False)
class Program(Loop):

    def to_bf_code(self):
        return ''.join(node.to_bf_code() for node in self.contains)  #type: ignore
