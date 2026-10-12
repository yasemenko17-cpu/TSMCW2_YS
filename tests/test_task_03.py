"""Відкриті приклади 03 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(3)

PUBLIC = [('quality_report',
  ([{'name': 'auth', 'loc': 2000, 'defects': 9, 'escaped': 3, 'statements': 400, 'covered': 380},
    {'name': 'billing',
     'loc': 4000,
     'defects': 8,
     'escaped': 1,
     'statements': 900,
     'covered': 630}],
   80,
   3),
  {'rows': [('auth', 4.5, 95.0, 33.3), ('billing', 2.0, 70.0, 12.5)],
   'attention': ['auth', 'billing'],
   'total': (2.83, 77.7)}),
 ('quality_report', ([], 80, 3), ('ValueError', 'Немає модулів'))]


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
    for name in ('quality_report',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
