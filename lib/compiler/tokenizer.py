# type: ignore
from types import GeneratorType
from funcparserlib.lexer import make_tokenizer, Token


BF_INSTRUCTIONS = "+-[].,<>"
TOKENS = [
    ('inc', (r"\++",)),
    ('dec', (r"-+",)),
    ('left', (r"<+",)),
    ('right', (r">+",)),
    ('loop_start', (r"\[",)),
    ('loop_end', (r"\]",)),
    ('output', (r"\.",)),
    ('input', (r",",)),
]


for token_name, details in TOKENS:
    globals()['t_%s' % token_name] = (
        lambda value=1, _name=token_name: Token(_name, value)
    )


def build_token_generator(code: str) -> GeneratorType:
    default_tokenizer = make_tokenizer(TOKENS)(
        ''.join(filter(lambda value: value in BF_INSTRUCTIONS, code))
    )
    for token in default_tokenizer:
        yield Token(token.type, len(token.value))
