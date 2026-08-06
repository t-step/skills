from app.reports.dispatcher import export_report


def test_csv():
    rows = [{"id": 1, "name": "Widget", "amount": 500}]
    assert export_report("csv", rows) == "id,name,amount\n1,Widget,500"


def test_pdf():
    rows = [{"id": 1, "name": "Widget", "amount": 500}]
    assert "PDF REPORT" in export_report("pdf", rows)


def test_unsupported():
    try:
        export_report("docx", [])
        assert False
    except ValueError:
        pass
