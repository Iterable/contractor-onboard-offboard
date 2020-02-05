"""Contractor onboarding Script v1.0.0
"""
import json
import os

from dotenv import load_dotenv  # Comment this line on prod

# Custom Module
from okta import Okta

load_dotenv()   #Comment this line on prod

# Environment Variables
ENV = os.environ['ENV']
GROUP_ID = os.environ['GROUP_ID']
OKTA_URL = os.environ['OKTA_URL']
OKTA_API_KEY = os.environ['OKTA_API_KEY']

def lambda_handler(event, context):
    """Basic Lambda Handler

    Returns:
        dict -- dictionary status code and message code
    """

    login_id = event['login_id']
    profile = {
        'firstName': event['first_name'],
        'lastName': event['last_name'],
        'secondEmail': event['secondary_email'],
        'manager': event['manager_name']
    }

    okta = Okta(OKTA_URL, OKTA_API_KEY)
    okta_id, okta_login_id, status = okta.create_user_by_profile(profile, login_id, 'ext')

    if status == 400:
        print("Login ID already exists in the the system. Try again with " + \
            "a different login_id.")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Login ID already exists in the the system. " + \
                    "Try again with a different login_id."
            })
        }

    okta.add_profile(okta_id, userType="Contractor")

    status = okta.add_user_to_group(okta_id, GROUP_ID)
    if status != 204:
        print("User created in OKTA but error adding the user to XYZ " + \
            "group. Exiting!")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "User created in OKTA but error adding the " + \
                    "user to XYZ group. Exiting!"
            })
        }
    status = okta.activate_user(okta_id)
    if status != 200:
        print("User created in Okta and added to group but was unable to " + \
            "be activated. Exiting!")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "User created in Okta and added to group but " + \
                    "was unable to be activated. Exiting!"
            })
        }
    print(f"Success! user {event['first_name']} {event['last_name']} with login {okta_login_id} " + \
                "has been created and activated successfully!")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Success! user {event['first_name']} {event['last_name']} with login {okta_login_id} " + \
                "has been created and activated successfully!"
        })
    }

def main(events, context):
    if ENV == 'prod':
        evnts = {}
        event_body = json.loads(events['body'])
        evnts['first_name'] = event_body['fields']['customfield_11130']
        evnts['last_name'] = event_body['fields']['customfield_11131']
        evnts['secondary_email'] = event_body['fields']['customfield_11080']
        evnts['manager_name'] = event_body['fields']['customfield_11044']['displayName']
        evnts['login_id'] = event_body['fields']['customfield_11128']
    else:
        evnts = {}
        evnts['first_name'] = "Test1"
        evnts['last_name'] = "test2"
        evnts['secondary_email'] = "test.test@gmail.com"
        evnts['manager_name'] = "tester tester"
        evnts['login_id'] = "test1.test2124"

    lambda_handler(evnts, {})

if __name__ == "__main__":
    main({}, {})