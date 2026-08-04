from app.search.query_parser import parse_query


def test_single_term():
    assert parse_query("hello") == {"must": ["hello"], "or": [], "fields": {}}


def test_multiple_terms_default_and():
    assert parse_query("hello world")["must"] == ["hello", "world"]


def test_or_terms():
    result = parse_query("cat OR dog")
    assert result["must"] == ["cat"]
    assert result["or"] == ["dog"]


def test_quoted_phrase():
    result = parse_query('"hello world"')
    assert result["must"] == ["hello world"]


def test_field_filter():
    result = parse_query("status:open")
    assert result["fields"] == {"status": "open"}


def test_field_filter_with_term():
    result = parse_query("status:open urgent")
    assert result["fields"] == {"status": "open"}
    assert result["must"] == ["urgent"]


def test_empty_query():
    assert parse_query("") == {"must": [], "or": [], "fields": {}}


def test_mixed_or_and_field():
    result = parse_query("status:open urgent OR blocked")
    assert result["fields"] == {"status": "open"}
    assert result["must"] == ["urgent"]
    assert result["or"] == ["blocked"]
