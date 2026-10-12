"""Відкриті приклади 05 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(5)

PUBLIC = [('choose_techniques',
  ({'goal': 'release_date', 'items': 40, 'history_sprints': 6, 'wants_probability': True},),
  ['Швидкість із діапазоном', 'Метод Монте-Карло']),
 ('choose_techniques', ({'goal': 'budget', 'items': 5},), ('ValueError', 'Невідома мета: budget'))]


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
    for name in ('choose_techniques',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
