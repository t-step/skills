from integration import _map_priority

def test_priority_mapping():
    assert _map_priority("critical") == 1
    assert _map_priority("low") == 4
    assert _map_priority("unknown") == 3
