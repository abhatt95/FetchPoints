# FetchPoints

API to manage collection and spending of FETCH points. Part of "Fetch take home challenge".


## Starting virtual environment to satisy any dependency. 
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

## balance
```
curl http://127.0.0.1:5000/api/v1/balance?id=<user-id>
```

Required query paramters
| Option      | Value |
| ----------- | ----------- |
| id      | User Id for which balance is requested. Data type: str       |

For a valid key  will return a valid JSON containing below key/value pairs.

| Key      | Value | Notes |
| ----------- | ----------- |----------- |
| status      | {"success"\|"failed"} Data type: str   | Response will always contains a status |
| message      | Possible reason for failure. Data type: str   | Only sent incase of failed status|
| data      |  Payer-points pair. Data type: json   | Only sent incase of success status|

Structure of payer-points -
```
{
"payer1" : 100,
"payer2" : 2000
}
```

Example of success -
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

Example of failure -
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
Messages for failure of balance call and possible resolution -
|message|resoluton|
|-----|-----|
|User ID is missing in request, please refer documentaion.|Please pass a valid user id in call.|
|User specified in query doesn't exist in system.|Balance doesn't exist for this user, no resolution can be provided.|

