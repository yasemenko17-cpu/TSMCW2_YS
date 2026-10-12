"""Відкриті приклади 10 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(10)

PUBLIC = [('ai_gate',
  ([{'id': 'PR-4',
     'risk': 'low',
     'ai_assisted': False,
     'lines': 30,
     'tests_pass': True,
     'tests_added': 0,
     'secrets_scan': True},
    {'id': 'PR-2',
     'risk': 'high',
     'ai_assisted': True,
     'ai_tool': 'Copilot',
     'ai_scope': 'тести',
     'log_entry': 'L-9',
     'author': 'ira',
     'reviewers': ['ira'],
     'ai_only_review': False,
     'lines': 150,
     'tests_pass': True,
     'tests_added': 0,
     'secrets_scan': True,
     'license_checked': False}],
   [{'id': 'L-2', 'decision': 'прийнято'}]),
  {'results': [('PR-4', 'пройшла', []),
               ('PR-2',
                'не пройшла',
                ['зміна завелика (150 рядків, ліміт 120)',
                 'запису L-9 немає в журналі',
                 'автор не може бути рецензентом',
                 'потрібно незалежних рецензентів: 2, є 0',
                 'немає жодного нового тесту',
                 'не перевірено ліцензії та збіги з публічним кодом'])],
   'passed': ['PR-4'],
   'failed': ['PR-2'],
   'ai_share': 50.0,
   'unused_log': ['L-2'],
   'summary': 'Пройшли браму: 1 з 2'}),
 ('ai_gate', ([], []), ('ValueError', 'Немає змін')),
 ('ai_gate',
  ([{'id': 'PR-1', 'risk': 'low', 'lines': 10, 'tests_added': 0}], None),
  ('ValueError', 'Некоректний журнал'))]


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
    for name in ('ai_gate',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
