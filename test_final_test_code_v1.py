import pytest
from unittest.mock import patch
import sys
from your_module import subtract_numbers  # Assuming your code is saved as your_module.py
def test_subtract_numbers_positive():
    assert subtract_numbers(10.5, 5.2) == 5.3
def test_subtract_numbers_negative():
    assert subtract_numbers(-10.5, -5.2) == -5.3
def test_subtract_numbers_mixed_signs():
    assert subtract_numbers(10.5, -5.2) == 15.7
    assert subtract_numbers(-10.5, 5.2) == -15.7
def test_subtract_numbers_zero():
    assert subtract_numbers(10.5, 0.0) == 10.5
    assert subtract_numbers(0.0, 5.2) == -5.2
    assert subtract_numbers(0.0, 0.0) == 0.0
def test_subtract_numbers_large_numbers():
    assert subtract_numbers(1e18, 1e-18) == 1e18
    assert subtract_numbers(1e-18, 1e18) == -1e18
def test_subtract_numbers_floating_point_precision():
    # Test cases where floating point arithmetic might be tricky
    assert subtract_numbers(0.1, 0.2) == pytest.approx(-0.1)
    assert subtract_numbers(0.3, 0.1) == pytest.approx(0.2)
def test_subtract_numbers_identity():
    assert subtract_numbers(7.8, 7.8) == 0.0
@pytest.mark.parametrize("num1, num2, expected", [
    (10, 5, 5),
    (-10, -5, -5),
    (10, -5, 15),
    (-10, 5, -15),
    (0, 5, -5),
    (5, 0, 5),
    (0, 0, 0),
    (1.5, 0.5, 1.0),
    (0.1, 0.2, -0.1),
])
def test_subtract_numbers_various_inputs(num1, num2, expected):
    assert subtract_numbers(float(num1), float(num2)) == pytest.approx(float(expected))
@patch('builtins.input', side_effect=['abc', '5'])
@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_main_invalid_first_input(mock_stderr, mock_stdout):
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    assert "Error: Invalid input. Please enter valid numbers." in mock_stderr.getvalue()
@patch('builtins.input', side_effect=['10', 'xyz'])
@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_main_invalid_second_input(mock_stderr, mock_stdout):
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    assert "Error: Invalid input. Please enter valid numbers." in mock_stderr.getvalue()
@patch('builtins.input', side_effect=['10', '5'])
@patch('sys.stdout', new_callable=StringIO)
def test_main_valid_input(mock_stdout):
    main()
    output = mock_stdout.getvalue()
    assert "-----------------------------------" in output
    assert "   Number Subtraction Program      " in output
    assert "Enter the first number: " in output
    assert "Enter the second number: " in output
    assert "\n10.0 - 5.0 = 5.0" in output
    assert "-----------------------------------" in output
@patch('builtins.input', side_effect=['-10.5', '-5.2'])
@patch('sys.stdout', new_callable=StringIO)
def test_main_negative_numbers(mock_stdout):
    main()
    output = mock_stdout.getvalue()
    assert "\n-10.5 - -5.2 = -5.3" in output
@patch('builtins.input', side_effect=['0', '0'])
@patch('sys.stdout', new_callable=StringIO)
def test_main_zero_input(mock_stdout):
    main()
    output = mock_stdout.getvalue()
    assert "\n0.0 - 0.0 = 0.0" in output
@patch('builtins.input', side_effect=['1000000000000000000', '0.000000000000000001'])
@patch('sys.stdout', new_callable=StringIO)
def test_main_large_numbers(mock_stdout):
    main()
    output = mock_stdout.getvalue()
    assert "\n1e+18 - 1e-18 = 1e+18" in output
@patch('builtins.input', side_effect=['0.1', '0.2'])
@patch('sys.stdout', new_callable=StringIO)
def test_main_floating_point_precision(mock_stdout):
    main()
    output = mock_stdout.getvalue()
    # Using approximation for floating point comparison in output
    assert re.search(r"\n0.1 - 0.2 = -0.1", output) is not None
from io import StringIO
import re
# Need to import StringIO for mocking stdout/stderr
# And re for pattern matching in the output string
```