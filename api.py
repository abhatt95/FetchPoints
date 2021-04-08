import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

users = {
    123 : {
        "c1" : 1,
        "c2" : 2
    }
}

# Constants 
ID = 'id'

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

app.run()
