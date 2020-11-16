from typing import Optional

from lib.ast import (Add, BaseASTNode, Dec, Drop, Inc, Left, Loop, Mul,
                     Program, Right, Sub)


class PlaceHolder(int):
    def __eq__(self, other: int):
        self.value: Optional[int] = other
        return True


def optimize_add_forward(loop: Loop) -> Optional[Add]:
    ph_0 = PlaceHolder()
    ph_1 = PlaceHolder()
    pattern = [Dec(1), Right(ph_0), Inc(1), Left(ph_1)]
    if pattern == loop.contains and ph_0.value == ph_1.value:  # type: ignore
        return Add(shift=ph_0.value)  # type: ignore


def optimize_add_reverse(loop: Loop) -> Optional[Add]:
    p0 = PlaceHolder()
    p1 = PlaceHolder()
    pattern = [Dec(1), Left(p0), Inc(1), Right(p1)]
    if pattern == loop.contains and p0.value == p1.value:  # type: ignore
        return Add(shift=-p0.value)  # type: ignore
    return None


def optimize_sub_forward(loop: Loop) -> Optional[Sub]:
    p0 = PlaceHolder()
    p1 = PlaceHolder()
    pattern = [Dec(1), Right(p0), Dec(1), Left(p1)]
    if pattern == loop.contains and p0.value == p1.value:  # type: ignore
        return Sub(shift=p0.value)  # type: ignore


def optimize_sub_reverse(loop: Loop) -> Optional[Sub]:
    p0 = PlaceHolder()
    p1 = PlaceHolder()
    pattern = [Dec(1), Left(p0), Dec(1), Right(p1)]
    if pattern == loop.contains and p0.value == p1.value:  # type: ignore
        return Sub(shift=-p0.value)  # type: ignore


def optimize_mul(loop: Loop) -> Optional[Mul]:
    # [->+++>+++++++<<]
    # mem[p+1] += mem[p] * 3;
    # mem[p+2] += mem[p] * 7;
    # mem[p] = 0
    p0 = PlaceHolder()
    p1 = PlaceHolder()
    p2 = PlaceHolder()
    p3 = PlaceHolder()
    p4 = PlaceHolder()
    pattern = [Dec(1), Right(p0), Inc(p1), Right(p2), Inc(p3), Left(p4)]
    if pattern == loop.contains and p0.value + p2.value == p4.value:  # type: ignore
        return Mul(
            shift0=p0.value, shift1=p0.value+p2.value,  # type: ignore
            mul0=p1.value, mul1=p3.value  # type: ignore
        )


def optimize_add(node: Loop) -> Optional[Add]:
    return optimize_add_forward(node) or optimize_add_reverse(node)


def optimize_sub(node: Loop) -> Optional[Sub]:
    return optimize_sub_forward(node) or optimize_sub_reverse(node)


def optimize_drop(loop: Loop) -> Optional[Drop]:
    pattern = [Dec(1), ]
    if pattern == loop.contains:
        return Drop()


OPTIMIZATIONS = [optimize_drop, optimize_mul, optimize_add, optimize_sub]


def optimize(node: BaseASTNode) -> BaseASTNode:
    if isinstance(node, Program):
        return Program(
            contains=[optimize(subnode) for subnode in node.contains]
        )
    elif isinstance(node, Loop):
        for optimization in OPTIMIZATIONS:
            result = optimization(node)
            if result:
                return result
        return Loop(
            contains=[optimize(subnode) for subnode in node.contains]
        )
    else:
        return node
