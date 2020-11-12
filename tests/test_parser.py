import os
import pytest


from lib.compiler import build_token_generator, p_program
from lib.compiler.tokenizer import BF_INSTRUCTIONS


CODE = list()


ASSETS_PREFIX = 'tests/assets/'
for root, dirs, files in os.walk(ASSETS_PREFIX):
    for filename in files:
        if filename.endswith('.b'):
            with open(os.path.join(ASSETS_PREFIX, filename)) as code_file:
                CODE.append((filename, code_file.read()))


@pytest.mark.parametrize("filename,code", CODE)
def test_parser(filename,code):
    code = ''.join(char for char in code if char in BF_INSTRUCTIONS)
    assert p_program.parse(tuple(build_token_generator(code))).to_bf_code() == code
