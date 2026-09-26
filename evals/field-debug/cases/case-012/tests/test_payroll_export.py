from payroll_export import build_record

def test_record_is_fixed_width():
    employee = {"employee_id": "E1002", "name": "Alan Turing", "net_pay": "184233"}
    record = build_record(employee)
    assert len(record) == 8 + 30 + 12  # passes: fixture name is pure ASCII
