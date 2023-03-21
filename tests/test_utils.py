from validator.util import validate_input
import pytest

@pytest.mark.parametrize("test_input,expected", [("dag_4: Trysil", True), ("dag 4: Trysil fjellet", False), ("1 dag 4: Trysil", False)])
def test_input_validation(test_input, expected):
    assert expected == validate_input(test_input)

