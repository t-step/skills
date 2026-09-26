# Nightly orders-vs-warehouse reconciliation -- 2026-09-24 run

| Metric                              | Count  |
|--------------------------------------|-------:|
| Orders placed (orders-svc)          | 40,118 |
| Orders pushed successfully           | 40,104 |
| Orders in `sync_errors.jsonl`        |     14 |
| Orders confirmed at warehouse intake | 38,918 |
| **Unaccounted gap**                  | **1,186** |

"Unaccounted gap" = orders `orders-svc` believes it pushed successfully
(i.e., not in the dead-letter file) that never show up in the warehouse's
own intake count for the same batch window. This gap has held steady at
roughly 3% of nightly volume for the last two weeks; before that it was
consistently under 0.1%.
