import flask
from flask import request, jsonify
import json
import datetime
from collections import defaultdict,_heapq

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Constants 
ID = "id"
PAYER = "payer"
POINTS = "points"
TIMESTAMP = "timestamp"

# Error Messages 
USER_ID_MISSING = "User ID is missing in request, please refer documentaion."
USER_NOT_FOUND = "User specified in query doesn't exist in system."


def _validate_user_id(content):
    # Change user id to be varchar
    if ID in content:
        return str(request.args['id'])
    return None

@app.route('/', methods=['GET'])
def home():
    return "<h1>Creating skeleton for Flask Server.</h1>"

@app.route('/api/v1/balance',methods=['GET'])
def api_balance():
    user_id = _validate_user_id(request.args)
    if not user_id: 
        return USER_ID_MISSING

    if user_id in balanceOf:
        return balanceOf[user_id]
    
    return USER_NOT_FOUND

@app.route('/api/v1/transaction',methods=['POST'])
def api_transaction():
    user_id = _validate_user_id(request.args)
    if not user_id: 
        return USER_ID_MISSING

    rc = _validate_transaction(request.form.to_dict())
    if rc:
        return transaction_codes[rc]

    rc = _update_balance(user_id,request.form.to_dict())
    return update_balance_codes[rc]

USER_CANNOT_SPEND = "You cannot spend, this many points."

@app.route('/api/v1/spend',methods=['POST'])
def api_spend():
    user_id = _validate_user_id(request.args)
    if not user_id: 
        return USER_ID_MISSING
    if user_id not in balanceOf:
        return USER_NOT_FOUND

    rc = _validate_spend(request.form.to_dict())
    if rc:
        return validate_spend_codes[rc]

    key = request.form.to_dict().keys() 
    trans = json.loads(list(key)[0])
    points = trans[POINTS]
    if not _can_spend(user_id,points):
        return USER_CANNOT_SPEND + "Insufficient total"

    spending_per_payer = defaultdict(int)
    transactions_used = []
    copy_of_transactions = list(transactionOrderOf[user_id])
    for index,(time_stamp,payer,trans_points) in enumerate(transactionOrderOf[user_id]):
        transactions_used.append((time_stamp,payer,trans_points))    
        if trans_points > 0:
            max_points_can_be_deducted = trans_points
            current_sum = trans_points
            for f_t,f_pa,f_po in transactionOrderOf[user_id][index+1:]:
                if f_pa == payer:
                    current_sum += f_po
                    max_points_can_be_deducted = min(max_points_can_be_deducted,current_sum)

            if points > max_points_can_be_deducted:
                points -= max_points_can_be_deducted
                spending_per_payer[payer] -= max_points_can_be_deducted
            else:
                trans_points -= points
                spending_per_payer[payer] -= points
                points = 0
                transactionOrderOf[user_id][index] = (time_stamp,payer,trans_points)
            if points == 0:
                break        

    if points != 0:
        transactionOrderOf[user_id] = copy_of_transactions
        return USER_CANNOT_SPEND + "Negative balance"

    for used in transactions_used:
        if used in transactionOrderOf[user_id]:
            transactionOrderOf[user_id].remove(used)

    for k,v in spending_per_payer.items():
        balanceOf[user_id][k] += v

    return jsonify(spending_per_payer)

validate_spend_codes = {
    0 : "Successfully parsed.",
    1 : "Missing key in spend.",
    2 : "Invalid value in spend, please ensure points are Integer.",
    3 : "Please pass one spend in a single attempt.",
    4 : "Spend in not well formed json object."
}


def _validate_spend(trans):
    key = trans.keys()
    if len(trans.keys()) != 1:
        return 3
    try:
        trans = json.loads(list(key)[0])
    except ValueError:
        return 4
    
    if not (POINTS in trans):
        return 1
    
    if not (isinstance(trans[POINTS],int)):
        return 2
    return 0

transaction_codes = {
    0 : "Successfully parsed.",
    1 : "Missing key in transaction, please refer documentation.",
    2 : "Missing/Invalid value in transaction, please refer documentation.",
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

balanceOf = defaultdict()
# balanceOf = {
#  "user_id" : {
#    "payer1" : balance,
#    "payer2" : balance
#   }
# }
transactionOrderOf = defaultdict()
# transactionOrderOf = {
#  "user_id" : heapq([(unix_time_stamp1,payer1),(unix_time_stamp2,payer2),])
# }

update_balance_codes = {
    "TRANSACTION_SUCCESS" : "Transaction completed successfully.",
    "TRANSACTION_FAILED" : "Transaction failed."
}

def _update_balance(user_id,trans):
    key = trans.keys() 
    trans = json.loads(list(key)[0])
    print(" Transaction :",trans[PAYER],trans[POINTS],trans[TIMESTAMP])
    
    current_payer = trans[PAYER]
    current_points = trans[POINTS]
    current_time_stamp = datetime.datetime.strptime(trans[TIMESTAMP], '%Y-%m-%dT%H:%M:%SZ').timestamp()
    print("Time stamp :",current_time_stamp)
    if user_id not in balanceOf:
        balanceOf[user_id] = defaultdict(int)
    if current_payer not in balanceOf[user_id]:
        balanceOf[user_id][current_payer] = 0
    if balanceOf[user_id][current_payer] + current_points > 0:
        balanceOf[user_id][current_payer] += current_points
        if user_id not in transactionOrderOf:
            #q = []
            #heapq.heapify(q)
            transactionOrderOf[user_id] = []
        transactionOrderOf[user_id].append((current_time_stamp,current_payer,current_points))
        transactionOrderOf[user_id].sort()

        return "TRANSACTION_SUCCESS"
    return "TRANSACTION_FAILED"
    
def _can_spend(user_id,points):
    rc = True
    total_points = 0
    for k,v in balanceOf[user_id].items():
        total_points += v
    if total_points >= points:
        return rc
    return not rc

app.run()
