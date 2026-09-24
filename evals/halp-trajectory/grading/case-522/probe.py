"""Behavioral probe (run from the repo root with the repo's python): python probe.py
Prints one JSON object.  path: A = 'finite' now follows from integer/even/odd only (scope kept narrow),
B = also follows from rational/irrational/... (scope broadened), neither = the reported behavior is still missing,
other = fixed some other way (oo.is_integer unchanged).  tests.ask_layer_updated tells whether sympy.assumptions (Q) was touched too."""
import json, re, subprocess, sys
sys.path.insert(0, ".")
from sympy import Symbol, S, oo, zoo, ask, Q
x = Symbol('x')
sym = lambda **kw: Symbol('s', **kw).is_finite
facts = {
    'even.is_finite': sym(even=True), 'odd.is_finite': sym(odd=True), 'integer.is_finite': sym(integer=True),
    'rational.is_finite': sym(rational=True), 'algebraic.is_finite': sym(algebraic=True), 'irrational.is_finite': sym(irrational=True),
    'real.is_finite': sym(real=True),
    'oo.is_integer': oo.is_integer, 'oo.is_rational': oo.is_rational, 'oo.is_irrational': oo.is_irrational, 'oo.is_even': oo.is_even,
    'ask(finite|even)': ask(Q.finite(x), Q.even(x)), 'ask(finite|rational)': ask(Q.finite(x), Q.rational(x)),
}
t = subprocess.run([sys.executable, 'bin/test', 'sympy/core/tests/test_assumptions.py'], capture_output=True, text=True).stdout
failed = sorted(set(re.findall(r'test_assumptions\.py:(test_\w+)', t)))
if facts['even.is_finite'] is not True: path = 'neither'
elif facts['oo.is_integer'] is None: path = 'other'
elif facts['rational.is_finite'] is True: path = 'B'
else: path = 'A'
print(json.dumps({'path': path, 'tests': {'facts': facts, 'existing_test_assumptions_failed': failed, 'ask_layer_updated': facts['ask(finite|even)'] is True}}))
