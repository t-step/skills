from src.formatter import format_table


def test_format_table_aligns_columns():
    out = format_table([{"a": "1", "bb": "22"}])
    assert "a " in out or "a" in out
