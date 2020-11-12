# type: ignore
import click
import jinja2


from lib.ast import Program
from lib.compiler import tokenizer, parser, generator


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    help='WTF compiler.'
)
@click.option(
    '-i', '--input', required=True,
    help='Path to bf source to compile.', type=click.File()
)
@click.option(
    '-t', '--template', required=True,
    help='Path to ASM src template', type=click.File()
)
def main(input, template):
    ast: Program = parser.p_program.parse(
        tuple(tokenizer.build_token_generator(input.read()))
    )
    click.echo(
        jinja2
            .Template(template.read(), trim_blocks=True, lstrip_blocks=True)
            .render({"commands": generator.visit_Program(ast)})
    )


if __name__ == "__main__":
    main()
