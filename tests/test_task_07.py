"""Відкриті приклади 07 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(7)

PUBLIC = [('decide_bet',
  ({'control': {'users': 1000, 'converted': 500},
    'variant': {'users': 1000, 'converted': 570},
    'min_effect': 5,
    'planned_sample': 1000},),
  {'decision': 'Масштабувати ставку',
   'uplift_pp': 7.0,
   'z': 3.14,
   'belief': 'Переконання підтверджено'}),
 ('decide_bet',
  ({'control': {'users': 0, 'converted': 0},
    'variant': {'users': 1000, 'converted': 500},
    'min_effect': 5,
    'planned_sample': 1000},),
  ('ValueError', 'Некоректна група: control'))]


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
    for name in ('decide_bet',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
