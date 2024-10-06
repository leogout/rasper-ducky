import pytest
from preprocessor import Preprocessor  # Assurez-vous que c'est le bon chemin d'importation

@pytest.fixture
def preprocessor():
    return Preprocessor()

def test_simple_define(preprocessor):
    code = """
    DEFINE MAX_VALUE 100
    VAR $x = MAX_VALUE
    """
    expected = """
    VAR $x = 100
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_multiple_defines(preprocessor):
    code = """
    DEFINE MAX 100
    DEFINE MIN 0
    VAR $x = MAX
    VAR $y = MIN
    """
    expected = """
    VAR $x = 100
    VAR $y = 0
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_define_with_expression(preprocessor):
    code = """
    DEFINE DOUBLE_MAX 100 * 2
    VAR $x = DOUBLE_MAX
    """
    expected = """
    VAR $x = 100 * 2
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_define_not_replacing_substrings(preprocessor):
    code = """
    DEFINE MAX 100
    VAR $x = MAX
    VAR $y = MAXIMUM
    """
    expected = """
    VAR $x = 100
    VAR $y = MAXIMUM
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_define_case_sensitivity(preprocessor):
    code = """
    DEFINE max 100
    VAR $x = max
    VAR $y = MAX
    """
    expected = """
    VAR $x = 100
    VAR $y = MAX
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_multiple_uses_of_define(preprocessor):
    code = """
    DEFINE VALUE 42
    VAR $x = VALUE
    VAR $y = VALUE + 1
    VAR $z = VALUE * 2
    """
    expected = """
    VAR $x = 42
    VAR $y = 42 + 1
    VAR $z = 42 * 2
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_define_order(preprocessor):
    code = """
    VAR $x = VALUE
    DEFINE VALUE 100
    VAR $y = VALUE
    """
    expected = """
    VAR $x = VALUE
    VAR $y = 100
    """
    assert preprocessor.process(code).strip() == expected.strip()

def test_redefine(preprocessor):
    code = """
    DEFINE VALUE 100
    VAR $x = VALUE
    DEFINE VALUE 200
    VAR $y = VALUE
    """
    expected = """
    VAR $x = 100
    VAR $y = 200
    """
    assert preprocessor.process(code).strip() == expected.strip()
