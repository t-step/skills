# Natural continuation after k=43 (django__django-14170, model46)  [reference data only]
- 44: `sed -n 100,180p test_extract_trunc.py`; text: the [iso_year] subtests "were written expecting the (broken) BETWEEN optimization"; "since the instructions say not to modify test files ... the 6 test failures are expected".
- 45-46: runs `lookup` and `model_fields` test modules (pass).
- 47-48: `git diff` -> patch.txt, submit. Final diff byte-identical to the k=43 diff; the 6 existing failures remain.
- Gold (upstream): `year_lookup_bounds_for_date_field/_datetime_field(value, iso_year=False)` compute ISO-year bounds with `fromisocalendar`; `YearLookup.year_lookup_bounds` passes `iso_year=isinstance(self.lhs, ExtractIsoYear)`; adds test_extract_iso_year_func_boundaries.
