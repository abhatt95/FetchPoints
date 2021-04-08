#!/bin/sh

# To execute -
# bash -x verify_inputs.sh 

# Positice cases : Valid id.
curl http://127.0.0.1:5000/api/v1/balance?id=12

curl http://127.0.0.1:5000/api/v1/balance?id=abc

# Negative cases : Invalid id. 
curl http://127.0.0.1:5000/api/v1/balance?id=

curl http://127.0.0.1:5000/api/v1/balance?

curl http://127.0.0.1:5000/api/v1/balance

# Positive case : Valid transaction. 
curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }'

# Negative cases : Invalid transaction.
curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000, "timestamp": "" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000}'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000, "timestamp":  }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T" }'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "", "points": 1000}'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": , "points": 1000}'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON" , "points": 1000.5, "timestamp": "2020-11-02T14:00:00Z"}'

curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "DANNON" , "points": , "timestamp": "2020-11-02T14:00:00Z"}'




# We need to look forward to see how many negative transations are there in future, to see how low a balance can go. 
# Now th lowest point >= 0 can be deducted from current transaction. And not more. 
# Once we have mapping of how much to reduce from which payer. We can update balanceOf.


# curl http://127.0.0.1:5000/api/v1/balance?id=123

# curl http://127.0.0.1:5000/api/v1/spend?id=123 -d '{"points":5000}'


# curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=123 -d '{ "payer": "UNILEVER", "points": -300, "timestamp": "2020-10-31T10:00:00Z" }'


# Make a queue of transaction for each user

# u1 [(timestamp,payer,points)]

# look at running sum of points till end of queue for current payer. 
# the lowest value it gets can be the most we can spend right now. After that this transaction has to be popped out. 
# Negative transactions are directly popped off as they are compensated by previously unused positive transaction. 

