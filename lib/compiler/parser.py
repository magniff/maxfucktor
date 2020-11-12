# type: ignore
from funcparserlib import parser as p
from lib import ast
from . import tokenizer as t


def build_simple_parser(token_name, ast_class):
    return (
        p.some(lambda token: token.type == token_name) >>
        (
            lambda token: ast_class(repeat=token.value)
        )
    )


p_inc = build_simple_parser(token_name='inc', ast_class=ast.Inc)
p_dec = build_simple_parser(token_name='dec', ast_class=ast.Dec)
p_right = build_simple_parser(token_name='right', ast_class=ast.Right)
p_left= build_simple_parser(token_name='left', ast_class=ast.Left)
p_input = build_simple_parser(token_name='input', ast_class=ast.Input)
p_output= build_simple_parser(token_name='output', ast_class=ast.Output)
p_simple_expression = p_dec | p_inc | p_right | p_left | p_input | p_output

p_loop_expression = p.forward_decl()
p_expression = p.forward_decl()
p_loop_expression.define(
    (
        p.skip(p.a(t.t_loop_start())) +
        p.maybe(p_expression) +
        p.skip(p.a(t.t_loop_end()))
    ) >>
    (
        lambda contains: ast.Loop(
            contains=(contains if contains else list())
        )
    )
)

p_expression.define(p.oneplus(p_simple_expression | p_loop_expression))
p_program = (
    p_expression >> (lambda contains: ast.Program(contains=contains))
)
