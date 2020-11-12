# type: ignore
from lib.ast.basic import Output
import click


from lib.ast import BaseASTNode, Program, Inc, Dec, Loop, Left, Right, Input, Output
from lib.compiler import tokenizer, parser


def format_node(node: BaseASTNode, maxlen: int, indent: int=0) -> str:
    if isinstance(node, Inc):
        return "  " * indent + "+" * node.repeat + "\n" # type: ignore
    elif isinstance(node, Dec):
        return "  " * indent + "-" * node.repeat + "\n" # type: ignore
    elif isinstance(node, Left):
        return "  " * indent + "<" * node.repeat + "\n" # type: ignore
    elif isinstance(node, Right):
        return "  " * indent + ">" * node.repeat + "\n" # type: ignore
    elif isinstance(node, Input):
        return "  " * indent + "," * node.repeat + "\n" # type: ignore
    elif isinstance(node, Output):
        return "  " * indent + "." * node.repeat + "\n" # type: ignore
    elif isinstance(node, Program):
        return (
            "  " * indent +
            "".join(format_node(n, maxlen=maxlen, indent=indent) for n in node.contains) # type: ignore
        )
    elif isinstance(node, Loop):
        bfcode = node.to_bf_code()
        if len(bfcode) <= maxlen:
            return "  " * indent + bfcode + "\n" # type: ignore
        return (
            "  " * indent +
            "[\n" +
                "".join(format_node(n, maxlen, indent+1) for n in node.contains) + "  " * indent +
            "]\n" # type: ignore
        )
    else:
        raise ValueError("Wtf is %s" % node)


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    help='WTF compiler.'
)
@click.option(
    '-i', '--input', required=True,
    help='Path to bf source to compile.', type=click.File()
)
@click.option(
    '-m', '--maxlen', required=False,
    help='Max loop length before line break', type=int, default=80
)
def main(input, maxlen: int):
    program: Program = parser.p_program.parse( # type: ignore
        tuple(
            tokenizer.build_token_generator(input.read()) # type: ignore
        )
    )
    click.echo(format_node(program, maxlen=maxlen))

if __name__ == "__main__":
    main()

