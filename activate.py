"""Contractor Activation Script v1.0.0
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

    okta = Okta(OKTA_URL, OKTA_API_KEY)
    okta_id = okta.get_user_by_login(login_id)


    status = okta.activate_user(okta_id)
    if status != 200:
        print(f"Unable to activate user {login_id}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Unable to activate user {login_id}"
            })
        }
    print(f"User {login_id} has been successfully activated!")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"User {login_id} has been successfully activated!"
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