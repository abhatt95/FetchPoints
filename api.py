import flask
from flask import request, jsonify
import json
import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

users = {
    123 : {
        "c1" : 1,
        "c2" : 2
    }
}

# Constants 
ID = "id"
PAYER = "payer"
POINTS = "points"
TIMESTAMP = "timestamp"

# Error Messages 
USER_ID_MISSING = "User ID is missing in request, please refer documentaion."
USER_NOT_FOUND = "User specified in query doesn't exist in system."



@app.route('/', methods=['GET'])
def home():
    return "<h1>Creating skeleton for Flask Server.</h1>"

@app.route('/api/v1/balance',methods=['GET'])
def api_balance():
    # Look for a User ID to return balance for.
    if ID in request.args:
        user_id = int(request.args['id'])
    else:
        return USER_ID_MISSING

    if user_id in users:
        return users[user_id]
    
    return USER_NOT_FOUND

transaction_error_codes = {
    0 : "Successfully parsed.",
    1 : "Missing key in transaction, please refer documentation.",
    2 : "Missing value in transaction, please refer documentation.",
    3 : "Please pass one transaction in a single attempt.",
    4 : "Transaction is not a well formed json object.",
    5 : "Invalid timestamp, please refer documentation."
}

def _validate_transaction(trans):
    key = trans.keys()
    if len(trans.keys()) != 1:
        return 3
    
    try:
        trans = json.loads(list(key)[0])
    except ValueError:
        return 4
    
    if not (PAYER in trans and POINTS in trans and TIMESTAMP in trans):
        return 1
    if not (len(trans[PAYER]) > 0 and  isinstance(trans[POINTS],int) and len(trans[TIMESTAMP]) > 0):
        return 2
    try:
        datetime.datetime.strptime(trans[TIMESTAMP], '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return 5

    return 0

@app.route('/api/v1/transaction',methods=['POST'])
def api_transaction():
    rc = _validate_transaction(request.form.to_dict())
    return transaction_error_codes[rc]

app.run()
