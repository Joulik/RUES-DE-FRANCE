import json
import logging

"""
This function is called by AWS every time the 
Submit button Lambda is triggered
"""

def handler(event, context):

    # define logging default level
    log_level = logging.DEBUG

    # update logging level if in AWS lambda
    if context:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)

    # parse the stringified json sent from javascript
    event = json.loads(event['body'])

    street_name = event['street_name']

    # function leading to subreports
    subreports = {"FR-C": 10, "FR-B": 12, "FR-A": 10, "FR-G": 9, "FR-F": 2,
    "FR-E": 1, "FR-D": 0, "FR-K": 15, "FR-J": 0, "FR-I": 7,
    "FR-YT": 7, "FR-O": 8, "FR-N": 3, "FR-M": 12, "FR-L": 2,
    "FR-S": 0, "FR-R": 0, "FR-Q": 12, "FR-P": 11, "FR-V": 9,
    "FR-U": 5, "FR-T": 5, "FR-RE": 0, "FR-GF": 1, "FR-H": 1,
    "FR-MQ": 4, "FR-GP": 4}

    #subreports = {'FR-60':1973}
    #print(subreports)

    return {
        'statusCode': 200,
        'body': json.dumps(subreports),
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Methods": "*"
        },
    }