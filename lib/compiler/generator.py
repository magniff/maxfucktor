import sys
import enum
from typing import Optional, Generator, Any


from dataclasses import dataclass


from lib.compiler.opt import optimize
from lib.ast import (
    BaseASTNode, Dec, Inc, Left, Output, Input,
    Program, Right, Loop, Add, Sub, Mul, Drop
)


GLOBAL_EXIT = "exit"


visitors = sys.modules[__name__]


def ids_generator():
    index = 0
    while True:
        yield "l%d" % index
        index += 1


ids = ids_generator()


@dataclass
class Command:
    pass


VisitorOutput = Generator[Command, Any, Any]


@dataclass
class CommandProceedLoop(Command):
    cont_id: str
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "proceed_%s:" % self.cont_id

    
@dataclass
class CommandInitLoop(Command):
    this_id: str
    cont_id: str
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "%s:" % self.this_id
        yield "cmp byte [r10], byte 0"
        yield "je %s" % self.cont_id


@dataclass
class CommandJump(Command):
    target_id: str
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "jmp %s" % self.target_id


@dataclass
class CommandLoopBack(Command):
    this_id: str
    cont_id: str
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "jmp %s" % self.this_id
        yield "%s:" % self.cont_id


@dataclass
class CommandRShift(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "add r10, %s" % self.repetitions


@dataclass
class CommandLShift(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "sub r10, %s" % self.repetitions


@dataclass
class CommandIncrement(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "add byte [r10], byte %s" % self.repetitions


@dataclass
class CommandDecrement(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "sub byte [r10], byte %s" % self.repetitions


@dataclass
class WriteSyscall(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        for _ in range(self.repetitions):
            yield "call do_write"


@dataclass
class ReadSyscall(Command):
    repetitions: int
    def to_asm(self) -> Generator[str, Any, Any]:
        for _ in range(self.repetitions):
            yield "call do_read"


@dataclass
class CommandMulCell(Command):
    shift0: int
    shift1: int
    mul0: int
    mul1: int

    def to_asm_block(self, mul_value: int, shift_value: int) -> Generator[str, Any, Any]:
        yield "movzx rax, byte [r10]"
        if mul_value > 1:
            yield "movzx r12, byte %s" % mul_value
            yield "mul r12b"
        yield "add byte [r10+%s], al" % shift_value

    def to_asm(self) -> Generator[str, Any, Any]:
        yield from self.to_asm_block(mul_value=self.mul0, shift_value=self.shift0)
        yield from self.to_asm_block(mul_value=self.mul1, shift_value=self.shift1)
        yield "mov [r10], byte 0"


@dataclass
class CommandResetCell(Command):
    def to_asm(self) -> Generator[str, Any, Any]:
        yield "mov byte [r10], byte 0"


class Op(enum.Enum):
    ADD = "add"
    SUB = "sub"


@dataclass
class CommandAddCell(Command):
    shift: int
    op: Op
    def to_asm(self) -> Generator[str, Any, Any]:
        skip_index = next(ids)
        yield "cmp byte [r10], byte 0"
        yield "je .skip%s" % skip_index
        yield "movzx r11, byte [r10]"
        yield "mov byte [r10], byte 0"
        yield "%s byte [r10+(%s)], r11b" % (self.op.value, self.shift)
        yield ".skip%s" % skip_index


def visit(node: BaseASTNode, cont_id: Optional[str]) -> VisitorOutput:
    yield from getattr(visitors, "visit_%s" % type(node).__qualname__)(node, cont_id)


def visit_Inc(node: Inc, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandIncrement(repetitions=node.repeat)


def visit_Dec(node: Dec, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandDecrement(repetitions=node.repeat)


def visit_Left(node: Left, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandLShift(repetitions=node.repeat)


def visit_Right(node: Right, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandRShift(repetitions=node.repeat)


def visit_Output(node: Output, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield WriteSyscall(node.repeat)


def visit_Input(node: Input, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield ReadSyscall(node.repeat)


def visit_Drop(_: Drop, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandResetCell()


def visit_Add(node: Add, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandAddCell(shift=node.shift, op=Op.ADD)


def visit_Sub(node: Sub, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandAddCell(shift=node.shift, op=Op.SUB)


def visit_Mul(node: Mul, *args, **kwargs) -> VisitorOutput: # type: ignore
    yield CommandMulCell(
        shift0=node.shift0, shift1=node.shift1, mul0=node.mul0, mul1=node.mul1
    )


def visit_Loop(node: Loop, cont_id: Optional[str]=None) -> VisitorOutput:
    this_id = next(ids)
    cont_id = cont_id or next(ids)

    if cont_id != GLOBAL_EXIT:
        yield CommandInitLoop(this_id=this_id, cont_id=cont_id) # type: ignore
    for subnode in node.contains:
        yield from visit(subnode, cont_id=None)
    if cont_id != GLOBAL_EXIT:
        yield CommandLoopBack(this_id=this_id, cont_id=cont_id) # type: ignore
    else:
        yield CommandJump(target_id=GLOBAL_EXIT)


def visit_Program(node: Program) -> VisitorOutput:
    yield from visit_Loop(optimize(node), cont_id=GLOBAL_EXIT) # type: ignore
