# FetchPoints

API to manage points collection and spending. Part of Fetch take home challenge.

# Starting service

We spin up a Flask server to handle all request. Run following commands to start service. 
```
virtualenv venv
python3 api.py
```

# API usage

All request and repsonse is in JSON format. 

## balance
```
curl http://127.0.0.1:5000/api/v1/balance?id=<user-id>
```
Returns the count of points accumulated for each payer for a user id. 

Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id for which balance is requested. Data type: str       |

Response 

| Key      | Value | Notes |
| ----------- | ----------- |----------- |
| status      | success/failed. Data type: str   | |
| message      | Possible reason for failure. Data type: str   | Only sent incase of failed status|
| data      |  Payer-points pair. Data type: json   | Only sent incase of success status|

Structure of payer-points -
```
{
"payer1" : 100,
"payer2" : 2000
}
```

Example of success 
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

Example of failure 
```
curl 'http://127.0.0.1:5000/api/v1/balance?id='
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


