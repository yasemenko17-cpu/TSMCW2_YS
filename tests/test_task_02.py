"""Відкриті приклади 02 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(2)

PUBLIC = [('check_ready',
  ({'text': 'Додати фільтр',
    'criteria': ['a', ' '],
    'points': 13,
    'dependencies': [{'name': 'API', 'resolved': False}, {'name': 'Дизайн', 'resolved': True}]},),
  {'ready': False,
   'problems': ['немає шаблону «Як..., я хочу..., щоб...»',
                'критеріїв прийняття менше трьох: 1',
                'історія завелика (13): розбийте її',
                'залежність API не вирішена'],
   'verdict': 'Повернути власнику продукту'}),
 ('check_ready', ([],), ('ValueError', 'Некоректна історія'))]


def _check(fn, args, expected):
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            getattr(M, fn)(*copy.deepcopy(args))
        assert str(info.value) == expected[1]
    else:
        assert getattr(M, fn)(*copy.deepcopy(args)) == expected


@pytest.mark.parametrize("fn,args,expected", PUBLIC, ids=[f"p{i}" for i in range(len(PUBLIC))])
def test_public(fn, args, expected):
    _check(fn, args, expected)


def test_functions_exist():
    for name in ('check_ready',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
