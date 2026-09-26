# `customer_export_job.py` (relevant excerpt, unchanged in 6+ weeks)

```python
from recordsdb_client import RecordsDB

db = RecordsDB(connection_string=EXPORT_DB_DSN)

def export_customer_records(customer_id):
    all_records = []
    page = db.query_page(customer_id, page_size=500)
    while page:
        all_records.extend(page.records)
        if not page.has_next:
            break
        page = db.query_page(customer_id, page_size=500, after=page.next_cursor)
    return all_records
```

`recordsdb-client` v4.2 (pinned in `requirements.txt`, unchanged in 6+
weeks). `page.next_cursor` is an opaque token the library derives from
the last row of the current page -- the job's own code never inspects or
constructs it directly.
