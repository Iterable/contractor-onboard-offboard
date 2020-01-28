"""Contractor onboarding Script v1.0.0
"""
import json
import os

import requests
from dotenv import load_dotenv
load_dotenv()

from Okta import Okta

ENV = os.environ['ENV']
GROUP_ID = os.environ['GROUP_ID']
OKTA_URL = os.environ['OKTA_URL']
OKTA_API_KEY = os.environ['OKTA_API_KEY']

def lambda_handler(event, context):
    """Basic Lambda Handler

    Returns:
        dict -- dictionary status code and message code
    """
    if ENV == 'PROD':
        evnts = json.loads(event['body'])
        firstname = evnts['first_name']
        lastname = evnts['last_name']
        login_id = evnts['login_id']
        secondary_email = evnts['secondary_email']
    else:
        firstname = "Jane1"
        lastname = "Doe1"
        login_id = "final.test"
        secondary_email = "shahisunny.47@gmail.com"

    okta = Okta(OKTA_URL,OKTA_API_KEY)
    okta_id, okta_login_id, status = okta.create_user(firstname, lastname, login_id,
                                                      secondary_email, ext=None)
    if status == 400:
        print("Login ID already exists in the the system. Try again with \
            a different login_id.")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Login ID already exists in the the system. \
                    Try again with a different login_id."
            })
        }
    status = okta.add_user_to_group(okta_id, GROUP_ID)
    if status != 204:
        print("User created in OKTA but error adding the user to XYZ \
            group. Exiting!")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "User created in OKTA but error adding the \
                    user to XYZ group. Exiting!"
            })
        }
    status = okta.activate_user(okta_id)
    if status != 200:
        print("User created in Okta and added to group but was unable to \
            be activated. Exiting!")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "User created in Okta and added to group but \
                    was unable to be activated. Exiting!"
            })
        }
    print(f"Success! user {firstname} {lastname} with login {okta_login_id} \
                has been created and activated successfully!")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Success! user {firstname} {lastname} with login {okta_login_id} \
                has been created and activated successfully!"
        })
    }

if __name__ == "__main__":
    lambda_handler({}, {})
