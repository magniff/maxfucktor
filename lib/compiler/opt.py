from lib.ast.basic import BaseASTNode
import sys
from typing import Optional
from lib.ast import Drop, Dec, Inc, Loop, Left, Right, Add, Sub, Program


optimizers = sys.modules[__name__]


class PlaceHolder(int):
    def __init__(self):
        self.value = None
    def __eq__(self, other: int):
        self.value = other
        return True


def optimize_add_forward(loop: Loop) -> Optional[Add]:
    ph_0 = PlaceHolder()
    ph_1 = PlaceHolder()
    pattern = [Dec(1), Right(ph_0), Inc(1), Left(ph_1)]
    if pattern == loop.contains and ph_0.value == ph_1.value: # type: ignore
        return Add(shift=ph_0.value) # type: ignore


def optimize_add_reverse(loop: Loop) -> Optional[Add]:
    ph_0 = PlaceHolder()
    ph_1 = PlaceHolder()
    pattern = [Dec(1), Left(ph_0), Inc(1), Right(ph_1)]
    if pattern == loop.contains and ph_0.value == ph_1.value: # type: ignore
        return Add(shift=-ph_0.value) # type: ignore
    return None


def optimize_sub_forward(loop: Loop) -> Optional[Sub]:
    ph_0 = PlaceHolder()
    ph_1 = PlaceHolder()
    pattern = [Dec(1), Right(ph_0), Dec(1), Left(ph_1)]
    if pattern == loop.contains and ph_0.value == ph_1.value: # type: ignore
        return Sub(shift=ph_0.value) # type: ignore


def optimize_sub_reverse(loop: Loop) -> Optional[Sub]:
    ph_0 = PlaceHolder()
    ph_1 = PlaceHolder()
    pattern = [Dec(1), Left(ph_0), Dec(1), Right(ph_1)]
    if pattern == loop.contains and ph_0.value == ph_1.value: # type: ignore
        return Sub(shift=-ph_0.value) # type: ignore


def optimize_add(node: Loop) -> Optional[Add]:
    return optimize_add_forward(node) or optimize_add_reverse(node)


def optimize_sub(node: Loop) -> Optional[Sub]:
    return optimize_sub_forward(node) or optimize_sub_reverse(node)


def optimize_drop(loop: Loop) -> Optional[Drop]:
    pattern = [Dec(1),]
    if pattern == loop.contains:
        return Drop()


OPTIMIZATIONS = [optimize_drop, optimize_add, optimize_sub ]


def optimize(node: BaseASTNode) -> BaseASTNode:
    if not isinstance(node, Loop):
        return node
    if isinstance(node, Program):
        return Program(
            contains=[optimize(subnode) for subnode in node.contains]
        )
    else:
        for optimization in OPTIMIZATIONS:
            result = optimization(node)
            if result:
                return result
        return Loop(
            contains=[optimize(subnode) for subnode in node.contains]
        )
