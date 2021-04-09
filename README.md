# FetchPoints

API to manage collection and spending of FETCH points. Part of "Fetch take home challenge".


## Starting virtual environment to satisfy dependency. 
```
virtualenv venv
```

# Starting service

We spin up a Flask server to handle all request. Run following commands to start service. 
> To learn more about [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
```
python3 api.py
```

# API usage

All request and repsonse are assumed to be valid JSON format. 

## 1. GET balance  
Returns current points/payer for a particular user.
## /api/v1/balance?id=\<user-id>
```
curl http://127.0.0.1:5000/api/v1/balance?id=<user-id>
```

### Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id for which balance is requested. <br/> Data type: str       |

### For a valid key request will return a valid JSON object containing below key/value pairs.

| Key      | Value | Notes |
| ----------- | ----------- |----------- |
| status      | {"success"\|"failed"} <br/> Data type: str   | Response will always contains a status |
| message      | Possible reason for failure. <br/> Data type: str   | Only sent incase of failed status|
| data      |  Payer-points pair. <br/> Data type: json   | Only sent incase of success status|

Structure of payer-points -
```
{
"payer1" : 100,
"payer2" : 2000
}
```

### Example of success -
```
curl 'http://127.0.0.1:5000/api/v1/balance?id=123'
{
  "data": {
    "DANNON": 2000, 
    "MILLER COORS": 5300, 
    "UNILEVER": 0
  }, 
  "status": "success"
}
```

### Example of failure -
```
curl 'http://127.0.0.1:5000/api/v1/balance?id=abc'
{
  "message": "User specified in query doesn't exist in system.", 
  "status": "failed"
}
 
curl 'http://127.0.0.1:5000/api/v1/balance?'
{
  "message": "User ID is missing in request, please refer documentaion.", 
  "status": "failed"
}
```
### Messages for failure of balance call and possible resolution if any -
|message|resoluton|
|-----|-----|
|User ID is missing in request, please refer documentaion.|Please pass a valid user id in call.|
|User specified in query doesn't exist in system.|Balance doesn't exist for this user.|

## 2. POST transaction  
Saves a single transaction for a user.
## /api/v1/transaction?id=\<user-id>
```
curl -XPOST http://127.0.0.1:5000/api/v1/transaction?id=<user-id> -d '{ "payer": "<payer-name>", "points": <points-int>, "timestamp": "<timestamp>" }'
```

### Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id for which transaction is posted. <br/> Data type: str       |

### Required key/value pair in data 
| Key      | Value |
| ----------- | ----------- |
| payer      | Name of payer involved in this transaction. <br/> Data type: str       |
| points      | Points modified in this transaction. <br/> Data type: int       |
| timestamp      | Time stamp of this transaction. <br/> Data type: time-stamp in following format - '%Y-%m-%dT%H:%M:%SZ'       |


### For a valid id and data, request will return a JSON object containing below key/value pairs.

| Key      | Value | Notes |
| ----------- | ----------- |----------- |
| status      | {"success"\|"failed"} <br/> Data type: str   | Response will always contains a status |
| message      | Possible reason for failure. <br/> Data type: str   | Only sent incase of failed status|


### Example of success -
```
curl -XPOST 'http://127.0.0.1:5000/api/v1/transaction?id=123' -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }'
{
  "status": "success"
}
```

### Example of failure -
```
curl -XPOST 'http://127.0.0.1:5000/api/v1/transaction?id=123' -d '{ "payer": "DANNON", "points": 1000, "timestamp":  }'
{
  "message": "Transaction is not a well formed json object.", 
  "status": "failed"
}

curl -XPOST 'http://127.0.0.1:5000/api/v1/transaction?id=123' -d '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T" }'
{
  "message": "Invalid timestamp, please refer documentation.", 
  "status": "failed"
}
```
### Messages for failure of transaction call and possible resolution if any -
|message|resoluton|
|-----|-----|
|Missing key in transaction, please refer documentation.| Please ensure all required key/val are passed in data for transaction.  |
|Missing/Invalid value in transaction, please refer documentation.|Please ensure all required key/val are passed in data for transaction.|
|Please pass one transaction in a single attempt.|Only one transaction can be procesed in one attempt, retry by passing single JSON object.|
|Transaction is not a well formed json object.|Ensure valid JSON object is passed in transaction data.|
|Invalid timestamp, please refer documentation.|Please pass time stamp of format '%Y-%m-%dT%H:%M:%SZ' , here Y - Year, m - Month, d - Day, H -Hour, M-Month, S-Second|
