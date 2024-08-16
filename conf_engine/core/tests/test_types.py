import conf_engine.core.types as types
import pytest


class TestString:
    def test_case_sensitive(self):
        t = types.String()
        assert t('String') != 'string'
        assert t('String') == 'String'

    def test_invalid_choices(self):
        t = types.String(choices=['string1', 'string2'])
        with pytest.raises(ValueError):
            assert t('string3')

    def test_case_sensitive_choices(self):
        t = types.String(choices=['string1', 'string2'])
        assert t('string1') == 'string1'
        with pytest.raises(ValueError):
            assert t('String2')

    def test_case_insensitive_choices(self):
        t = types.String(choices=['string1', 'string2'], ignore_case=True)
        assert t('String1') == 'string1'
        assert t('string2') == 'string2'


class TestNumber:
    def test_number(self):
        t = types.Number()
        assert t('12345') == 12345

    def test_integer(self):
        t = types.Integer()
        assert t('12345') == 12345

    def test_float(self):
        t = types.Float()
        assert t('1.2345') == 1.2345

    def test_is_integer_method(self):
        assert types.Number._is_integer('1')
        assert types.Number._is_integer(1)
        assert not types.Number._is_integer('string')

    def test_is_float_method(self):
        assert types.Number._is_float('1.5')
        assert types.Number._is_float(1.5)
        assert not types.Number._is_float('string')

    def test_is_number_method(self):
        assert types.Number._is_number('1.5')
        assert types.Number._is_number(1.5)
        assert types.Number._is_number('1.5')
        assert types.Number._is_number(1.5)
        assert not types.Number._is_number('string')

    def test_minimum(self):
            t = types.Number(minimum=10)
            assert t('10') == 10
            with pytest.raises(ValueError):
                assert t('9')

    def test_maximum(self):
        t = types.Number(maximum=10)
        assert t('10') == 10
        with pytest.raises(ValueError):
            assert t('11')

    def test_choices(self):
        choices = ['1', '2', '3']
        t = types.Number(choices=choices)
        for choice in choices:
            assert t(choice) == int(choice)

    def test_invalid_choice(self):
        t = types.Number(choices=['1', '2'])
        with pytest.raises(ValueError):
            assert t('3')

    def test_minimum_over_maximum(self):
        with pytest.raises(ValueError):
            assert types.Number(maximum=1, minimum=10)


class TestBoolean:
    def test_true_values(self):
        t = types.Boolean()
        assert t(True)
        assert t('yes')
        assert t('true')
        assert t('True')
        assert t(1)
        assert t('1')
        assert t('on')

    def test_false_values(self):
        t = types.Boolean()
        assert not t(False)
        assert not t('no')
        assert not t('No')
        assert not t('False')
        assert not t(0)
        assert not t('0')
        assert not t('off')

    def test_not_boolean(self):
        t = types.Boolean()
        with pytest.raises(ValueError):
            assert t('not boolean')

