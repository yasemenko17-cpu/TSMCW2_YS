"""Відкриті приклади 04 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(4)

PUBLIC = [('check_bets',
  ([{'name': 'Фільтри', 'appetite': 2, 'started': 1, 'finished': 2},
    {'name': 'Чат', 'appetite': 6, 'started': 1, 'finished': None},
    {'name': 'Оплата', 'appetite': 2, 'started': 3, 'finished': None}],
   5),
  {'rows': [('Фільтри', 'завершено вчасно', 2, 0),
            ('Чат', 'триває', 5, 1),
            ('Оплата', 'запобіжник', 3, 0)],
   'breaker': ['Оплата'],
   'overspend_weeks': 1,
   'next_step': 'Повернути на шейпінг: Оплата'}),
 ('check_bets',
  ([{'name': 'Чат', 'appetite': 6, 'started': 1, 'finished': None}], 0),
  ('ValueError', 'Некоректний тиждень'))]


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
    for name in ('check_bets',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
