#!/bin/sh

# To execute -
# bash -x verify_transaction.sh

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }'


curl http://127.0.0.1:5000/api/v1/balance?id=123

curl http://127.0.0.1:5000/api/v1/spend?id=123 -d '{"points":5000}'

curl http://127.0.0.1:5000/api/v1/balance?id=123


curl 'http://127.0.0.1:5000/api/v1/spend?id=123' -d '{"points":5000}'

curl 'http://127.0.0.1:5000/api/v1/spend?id=123' -d '{"points":2000}'

curl 'http://127.0.0.1:5000/api/v1/spend?id=123' -d '{"points":2000}'

curl http://127.0.0.1:5000/api/v1/balance?id=123