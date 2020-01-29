"""Contractor offboarding Script v1.0.0
"""
import json
import os

from dotenv import load_dotenv  # Comment this line on prod

from jira import Jira
from okta import Okta

load_dotenv()   #Comment this line on prod

OKTA_URL = os.environ['OKTA_URL']
OKTA_API_KEY = os.environ['OKTA_API_KEY']
ENV = os.environ['ENV']
JIRA_USER = os.environ['JIRA_USER']
JIRA_AUTH = os.environ['JIRA_AUTH']
JIRA_URL = os.environ['JIRA_URL']


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
    if okta_id is not None:
        if ENV == "PROD":
            jira = Jira(JIRA_USER, JIRA_AUTH, JIRA_URL)

            okta_logs, _ = okta.get_logs(okta_id)   # returns the log text and status code; using _
            summary = f"{login_id} has been deactivated from OKTA"
            body = f"{login_id} has been deactivated from OKTA and their okta log " + \
            "has been attached to this ticket."

            jira.create_issue_with_attachment(summary, body, okta_logs, "okta_logs.json")
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
