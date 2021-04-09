from collections import defaultdict
from flask import request, jsonify
import json
import datetime

# Constants 
ID = "id"
PAYER = "payer"
POINTS = "points"
TIMESTAMP = "timestamp"
STATUS = "status"
SUCCESS = "success"
FAILED = "failed"
MESSAGE = "message"
DATA = "data"

# Error Messages 
USER_ID_MISSING = "User ID is missing in request, please refer documentaion."
USER_NOT_FOUND = "User specified in query doesn't exist in system."