import pytest

import conf_engine.options as o


def test_string_option():
    """Test default values work and cast to string accordingly."""
    opt = o.StringOption('test_string_option')
    assert opt('string_value') == 'string_value'


def test_string_option_to_type_constructor():
    """Verify that all options are passed through to the type constructor."""
    max_length = 10
    choices = ['choice_one', 'choice_two']
    ignore_case = True
    opt = o.StringOption('test_string_option', max_length=max_length, choices=choices, ignore_case=ignore_case)
    assert opt.option_type._max_length == max_length
    assert opt.option_type._choices == choices
    assert opt.option_type._ignore_case == ignore_case


def test_number_option():
    """Test default values work and cast to int accordingly."""
    opt = o.NumberOption('test_number_option')
    assert opt('8675309') == 8675309


def test_number_option_to_type_constructor():
    """Verify that all options are passed through to the type constructor."""
    minimum = 0.38
    maximum = 0.45
    choices = [0.38, 0.44, 0.45]
    cast = float
    opt = o.NumberOption('test_number_option', minimum=minimum, maximum=maximum, choices=choices, cast=cast)
    assert opt.option_type._minimum == minimum
    assert opt.option_type._maximum == maximum
    assert opt.option_type._choices == choices
    assert opt.option_type._cast == cast


def test_boolean_option():
    """Test default values work and cast to bool accordingly."""
    opt = o.BooleanOption('test_boolean_option')
    assert opt('True') is True


def test_proper_default():
    o.NumberOption('test_string_option', default=55)


def test_improper_default():
    with pytest.raises(ValueError):
        o.NumberOption('test_string_option', default='a string')
