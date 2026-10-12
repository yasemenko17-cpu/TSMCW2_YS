"""Відкриті приклади 06 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(6)

PUBLIC = [('pyramid_report',
  ([{'name': 't1', 'seconds': 0.1},
    {'name': 't2', 'seconds': 0.2},
    {'name': 't3', 'seconds': 2, 'database': True},
    {'name': 't4', 'seconds': 90},
    {'name': 't5', 'seconds': 40, 'ui': True}],),
  {'levels': [('t1', 'модульний'),
              ('t2', 'модульний'),
              ('t3', 'інтеграційний'),
              ('t4', 'інтеграційний'),
              ('t5', 'наскрізний')],
   'counts': (2, 2, 1),
   'shares': (40.0, 40.0, 20.0),
   'shape': 'піраміда',
   'far_from_target': ['модульний', 'інтеграційний']}),
 ('pyramid_report', ([],), ('ValueError', 'Немає тестів'))]


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
    for name in ('pyramid_report',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
