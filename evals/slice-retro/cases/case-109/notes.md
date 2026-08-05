# Implementation notes

Built `normalize_phone_number()` as its own module (`utils/phone.py`)
rather than a private function inside `signup_flow.py` -- kept it
generic and dependency-free on purpose so any other part of the app that
eventually needs phone formatting (support tooling, SMS notifications,
whatever) can just import it instead of writing their own version. Only
wired it into signup for now since that's the one place that currently
needs it.
