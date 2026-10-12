"""Відкриті приклади 08 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(8)

PUBLIC = [('screen_request',
  ('Надішли звіт на anna@example.com, тел. 0501234567, тікет PRJ-4521',),
  {'action': 'redact',
   'found': ['телефон', 'email', 'внутрішній ідентифікатор'],
   'text': 'Надішли звіт на [EMAIL], тел. [ТЕЛЕФОН], тікет [ВНУТР_ID]',
   'replaced': 3}),
 ('screen_request', ('   ',), ('ValueError', 'Порожній запит'))]


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
    for name in ('screen_request',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
