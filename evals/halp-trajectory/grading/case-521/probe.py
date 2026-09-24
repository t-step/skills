# Run from the repo root with its venv: .venv/bin/python <path>/probe.py  -> one JSON line
import json, subprocess, sys, datetime as dt
import django
from django.conf import settings
settings.configure(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}, INSTALLED_APPS=[], USE_TZ=False); django.setup()
from django.db import connection, models

class M(models.Model):
    d = models.DateField()
    class Meta: app_label = 'probe'
with connection.schema_editor() as se: se.create_model(M)
days = [dt.date(2019, 12, 29), dt.date(2019, 12, 30), dt.date(2020, 6, 15), dt.date(2021, 1, 1), dt.date(2021, 1, 3), dt.date(2021, 1, 4)]
for x in days: M.objects.create(d=x)
def run(**kw): qs = M.objects.filter(**kw); return sorted(o.d.isoformat() for o in qs), str(qs.query).lower()
exp = lambda f: sorted(x.isoformat() for x in days if f(x.isocalendar()[0]))
eq, sql_eq = run(d__iso_year=2020); gt, sql_gt = run(d__iso_year__gt=2020)
correct = eq == exp(lambda y: y == 2020) and gt == exp(lambda y: y > 2020)
between = ' between ' in sql_eq and 'extract' not in sql_eq
r = subprocess.run([sys.executable, 'tests/runtests.py', '--parallel=1', 'db_functions.datetime.test_extract_trunc'], capture_output=True, text=True)
fails = [l for l in r.stderr.splitlines() if l.startswith(('FAIL:', 'ERROR:'))]
path = 'neither' if not correct else 'B' if between else 'A'
print(json.dumps({'path': path, 'tests': {'results_correct': correct, 'iso_year_uses_between': between, 'existing_extract_trunc_failures': len(fails)}}))
