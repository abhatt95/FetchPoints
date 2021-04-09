
from constants import *


def _validate_user_id(content):
    # Change user id to be varchar
    if ID in content:
        return str(request.args['id'])
    result = defaultdict()
    result[STATUS] = FAILED
    result[MESSAGE] = USER_ID_MISSING
    return jsonify(result)

USER_CANNOT_SPEND = "You cannot spend, this many points."

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

