"""Відкриті приклади 09 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(9)

PUBLIC = [('decide_change',
  ({'id': 'CR-1', 'type': 'problem', 'impact_days': 3, 'value': 6},
   {'reserve_days': 5, 'goal_at_risk': False}),
  {'id': 'CR-1',
   'decision': 'Затвердити',
   'reserve_after': 2,
   'rebaseline': False,
   'next_step': 'Виконати в межах резерву'}),
 ('decide_change',
  ({'id': 'CR-3', 'type': 'vendor', 'impact_days': 1, 'value': 5},
   {'reserve_days': 5, 'goal_at_risk': False}),
  ('ValueError', 'Некоректний запит: CR-3'))]


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
    for name in ('decide_change',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
