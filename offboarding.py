"""Contractor offboarding Script v1.0.0
"""
import json
import os

import requests
from dotenv import load_dotenv

from Okta import Okta

load_dotenv()

OKTA_URL = os.environ['OKTA_URL']
OKTA_API_KEY = os.environ['OKTA_API_KEY']
ENV = os.environ['ENV']


def lambda_handler(event, context):
    """Basic Lambda Handler

    Returns:
        dict -- dictionary status code and message code
    """
    if ENV == 'PROD':
        evnts = json.loads(event['body'])
        login_id = evnts['login_id']
    else:
        login_id = "final.test"

    okta = Okta(OKTA_URL, OKTA_API_KEY)

    okta_id = okta.get_user_by_login(login_id)
    if okta_id != None:
        status = okta.deactivate_user(okta_id)
        print("Deactivation successful!")
        return {
            "status": status
        }
    print("Error while deactivating user. Exiting!")
    return {
        "status" : 400,
        'body' : "Error while deactivating user"
    }


if __name__ == "__main__":
    lambda_handler({}, {})
