import json
import os

import requests

class Okta:
    """OKTA Class for interacting with the API

    """
    def __init__(self, okta_url, okta_api_key):
        self.OKTA_URL = okta_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'SSWS {}'.format(okta_api_key)
        }

    def get_user_by_login(self, login):

        url = self.OKTA_URL + f"/api/v1/users?q={login}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        try:
            return data[0]['id']
        except IndexError as e:
            print("Error:", e, "\nLogin_id not found in Okta.")

    def deactivate_user(self, okta_id):
        """Deactivate user from OKTA

        Arguments:
            okta_id {str} -- Okta user id

        Returns:
            int -- status code
        """
        url = self.OKTA_URL + f"/api/v1/users/{okta_id}/lifecycle/deactivate"

        response = requests.post(url, headers=self.headers)
        return response.status_code

    def create_user(self, firstname, lastname, login_id, secondary_email):
        """Creates the OKTA user

        Arguments:
            firstname {str} -- First Name
            lastname {str} -- Last Name
            login_id {str} -- Login ID, must be unique
            secondary_email {str} -- Email to send initial login information

        Returns:
            tuple -- returns OKTA id, the user full profile ID, and the status code
        """

        url = self.OKTA_URL + "/api/v1/users?activate=false"
        profile_json = {
            'profile': {
                'firstName': firstname,
                'lastName': lastname,
                'email': f'{login_id}@iterable.com',
                'login': f'{login_id}@iterable.com',
                'secondEmail': secondary_email
            }
        }
        response = requests.post(url, headers=self.headers, json=profile_json)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['id'], response_data['profile']['login'], response.status_code

        return None, None, response.status_code

    def add_user_to_group(self, user_id, group_id):
        """The function adds user to the group

        Arguments:
            user_id {str} -- OKTA id
            group_id {str} -- group ID

        Returns:
            int -- status code
        """
        url = self.OKTA_URL + f"/api/v1/groups/{group_id}/users/{user_id}"
        response = requests.put(url, headers=self.headers)
        return response.status_code

    def activate_user(self, user_id, is_email=True):
        """Activate the user

        Arguments:
            user_id {str} -- Okta user ID

        Keyword Arguments:
            isEmail {bool} -- Send activation (default: {True})

        Returns:
            int -- Status Code
        """
        if is_email is True:
            send_email = "true"
        else:
            send_email = "false"
        url = self.OKTA_URL + f"/api/v1/users/{user_id}/lifecycle/activate?sendEmail={send_email}"

        response = requests.post(url, headers=self.headers)
        return response.status_code
