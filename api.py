import flask
from flask import request, jsonify
import json
import datetime
from collections import defaultdict,_heapq
from validate_user_inputs import  *
from validate_user_inputs import _validate_user_id, _validate_spend, _validate_transaction
from spend_operations import *
from spend_operations import _update_balance, _can_spend
from spend_operations import _spend_points_

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Creating skeleton for Flask Server.</h1>"

@app.route('/api/v1/balance',methods=['GET'])
def api_balance():

    result = defaultdict()
    user_id = _validate_user_id(request.args)

    if not isinstance(user_id,str): 
        return user_id

    if user_id in balanceOf:
        result[STATUS] = SUCCESS
        result[DATA] = balanceOf[user_id]
        return jsonify(result)

    result[STATUS] = FAILED
    result[MESSAGE] = USER_NOT_FOUND
    return jsonify(result)

@app.route('/api/v1/transaction',methods=['POST'])
def api_transaction():

    result = defaultdict()
    user_id = _validate_user_id(request.args)

    if not isinstance(user_id,str): 
        return user_id

    rc = _validate_transaction(request.form.to_dict())
    if rc:
        result[STATUS] = FAILED
        result[MESSAGE] = transaction_codes[rc]
        return jsonify(result)

    rc = _update_balance(user_id,request.form.to_dict())
    if rc == "TRANSACTION_SUCCESS":
        result[STATUS] = SUCCESS 
    else:
        result[STATUS] = FAILED 
        result[MESSAGE] = update_balance_codes[rc]

    return jsonify(result)


@app.route('/api/v1/spend',methods=['POST'])
def api_spend():
    user_id = _validate_user_id(request.args)
    result = defaultdict()

    if not isinstance(user_id,str): 
        return user_id

    if user_id not in balanceOf:
            result[STATUS] = FAILED
            result[MESSAGE] = USER_NOT_FOUND
            return jsonify(result)

    rc = _validate_spend(request.form.to_dict())
    if rc:
        result[STATUS] = FAILED 
        result[MESSAGE] = validate_spend_codes[rc]
        return jsonify(result)

    key = request.form.to_dict().keys() 
    trans = json.loads(list(key)[0])
    points = trans[POINTS]

    if not _can_spend(user_id,points):
        result[STATUS] = FAILED 
        result[MESSAGE] = USER_CANNOT_SPEND
        return  jsonify(result)

    data = _spend_points_(user_id,points)

    if not data:
        result[STATUS] = FAILED 
        result[MESSAGE] = USER_CANNOT_SPEND
        return jsonify(result) 
    
    result[STATUS] = SUCCESS
    result[DATA] = data
    return jsonify(result)

app.run()