# FetchPoints

API to manage collecting and spending of FETCH points. Part of "Fetch take home challenge".

> Please install/ensure Python 3.7 is available before moving to next steps.  


## Setting up Python virtual environment for service 
Creating virtual environment
> [Reasons for using virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#:~:text=virtualenv%20is%20used%20to%20manage,can%20install%20virtualenv%20using%20pip.)
```
virtualenv venv
```
Activating environment 
```
source venv/bin/activate
```
Installing dependency 
```
pip install -r requirement.txt
```

# Starting service

We spin up a Flask server to handle all request. Run following commands to start service.
> To learn more about [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
```
python3 api.py
```

# API usage

All communication (request and repsonse) are assumed to be well formed JSON object. 
> Response JSON object for any call will contain "status" key. "status" will have two possible value - "success" , "failed". Incase of "failed" status, object will contain a key "message" who's value will provide detailed failure message. Incase of "success" status, object won't contain "message" key. Based on type of call, successfully executed call's response object may contain "data" as key and it's value would be result of call.

## 1. GET balance  
Returns current points stored for each payer for a particular user.
```
curl http://127.0.0.1:5000/api/v1/balance?id=<user-id>
```
[Skip to example](#example-of-success--) 
### Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id for which balance is requested. <br/> Data type: str       |

### Response is a valid JSON object containing some key/value pairs from below -

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

### Messages for failure of balance call and possible resolution if any -
|message|resoluton|
|-----|-----|
|User ID is missing in request, please refer documentaion.|Please pass a valid user id in call.|
|User specified in query doesn't exist in system.|Balance doesn't exist for this user.|

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

## 2. POST transaction  
Saves a single transaction passed as data for a given user.
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

### Messages for failure of transaction call and possible resolution if any -
|message|resoluton|
|-----|-----|
|Missing key in transaction, please refer documentation.| Please ensure all required key/val are passed in data for transaction.  |
|Missing/Invalid value in transaction, please refer documentation.|Please ensure all required key/val are passed in data for transaction.|
|Please pass one transaction in a single attempt.|Only one transaction can be procesed in one attempt, retry by passing single JSON object.|
|Transaction is not a well formed json object.|Ensure valid JSON object is passed in transaction data.|
|Invalid timestamp, please refer documentation.|Please pass time stamp of format '%Y-%m-%dT%H:%M:%SZ' , here Y - Year, m - Month, d - Day, H -Hour, M-Month, S-Second|


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

## 3. POST spend  
Saving points spent by user. 
```
curl http://127.0.0.1:5000/api/v1/spend?id=<user-id> -d '{"points":<points-spent>}'
```

### Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id of person spending points. <br/> Data type: str       |

### Required key/value pair in data 
| Key      | Value |
| ----------- | ----------- |
| points      | Number of points being spent by user. <br/> Data type: int       |


### For a valid id and data, request will return a JSON object containing below key/value pairs.

| Key      | Value | Notes |
| ----------- | ----------- |----------- |
| status      | {"success"\|"failed"} <br/> Data type: str   | Response will always contains a status |
| message      | Possible reason for failure. <br/> Data type: str   | Only sent incase of failed status|
| data      | Amount of points dedcuted from each payer in users account. <br/> Data type: JSON   | Only sent incase of success status|

Strcture of points dedcuted per payer -
```
{
"payer1" : -100,
"payer2" : -200
}
```

### Messages for failure of spend call and possible resolution if any -
|message|resoluton|
|-----|-----|
|Missing key in spend.|Please ensure all key/value pairs are passed.|
|Invalid value in spend, please ensure points are Integer.|Please ensure valid int is passed to spend points.|
|Spend in not well formed json object.|Please send well formed JSON as data to this call.|
|Please pass one spend in a single attempt.|Please pass single JSON object wit one points parameter at a given time.|

### Example of success -
```
 curl 'http://127.0.0.1:5000/api/v1/spend?id=123' -d '{"points":5000}'
{
  "data": {
    "DANNON": -100, 
    "MILLER COORS": -4700, 
    "UNILEVER": -200
  }, 
  "status": "success"
}
```

### Example of failure -
```
curl 'http://127.0.0.1:5000/api/v1/spend?id=123' -d '{"points":2000}'
{
  "message": "You cannot spend, this many points.", 
  "status": "failed"
}
```

