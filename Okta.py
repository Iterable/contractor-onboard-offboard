"""
Okta Module

written in python 3.8
"""
import json

import requests

class Okta:
    """OKTA Class for interacting with the API

    """
    def __init__(self, okta_url, okta_api_key):
        self.okta_url = okta_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'SSWS {}'.format(okta_api_key)
        }

    def get_user_by_login(self, login):
        """Retrieves user from the api using the login

        Arguments:
            login {str} -- Login_email

        Returns:
            str -- okta_id
        """
        url = self.okta_url + f"/api/v1/users?q={login}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        try:
            return data[0]['id']
        except IndexError as exception:
            print("Error:", exception, "\nLogin_id not found in Okta.")

    def suspend_user(self, okta_id):
        """Suspend Okta User

        Arguments:
            okta_id {str} -- Okta Unique ID

        Returns:
            int -- status code from the HTTP operation
        """
        url = self.okta_url + f"/api/v1/users/{okta_id}/lifecycle/suspend"
        response = requests.post(url, headers=self.headers)
        return response.status_code

    def deactivate_user(self, okta_id):
        """Deactivate user from OKTA

        Arguments:
            okta_id {str} -- Okta user id

        Returns:
            int -- status code
        """
        url = self.okta_url + f"/api/v1/users/{okta_id}/lifecycle/deactivate"

        response = requests.post(url, headers=self.headers)
        return response.status_code

    def create_user(self, firstname, lastname, login_id, secondary_email, ext=None):
        """Creates the OKTA user

        Arguments:
            firstname {str} -- First Name
            lastname {str} -- Last Name
            login_id {str} -- Login ID, must be unique
            secondary_email {str} -- Email to send initial login information

        Keyword Arguments:
            ext {str} -- Add optional description (default: {None})

        Returns:
            tuple -- returns OKTA id, the user full profile ID, and the status code
        """
        if ext is not None:
            email = f"{login_id}.{ext}@iterable.com"
        else:
            email = f"{login_id}@iterable.com"
        url = self.okta_url + "/api/v1/users?activate=false"
        profile_json = {
            'profile': {
                'firstName': firstname,
                'lastName': lastname,
                'email': email,
                'login': email,
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
        url = self.okta_url + f"/api/v1/groups/{group_id}/users/{user_id}"
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
        url = self.okta_url + f"/api/v1/users/{user_id}/lifecycle/activate?sendEmail={send_email}"

        response = requests.post(url, headers=self.headers)
        return response.status_code

    def add_profile(self, user_id, **kwargs):
        """Add data to the profile of the user

        Arguments:
            user_id {str} -- Okta user_id of the user to be updated

        Returns:
            int -- status code
        """
        url = self.okta_url + f"/api/v1/users/{user_id}"

        profile_data = {'profile':{}}
        for key, value in kwargs.items():
            profile_data['profile'][key] = value

        response = requests.post(url, headers=self.headers, json=profile_data)
        if response.status_code == 400:
            print(response.json()["errorCauses"][0]["errorSummary"])
        return response.status_code

    def get_logs(self, okta_id):
        response = requests.get('https://iterable.okta.com/api/v1/logs?filter=target.id+eq+"{0}"+or+actor.id+eq+"{0}"'.format(okta_id), headers=self.headers)
        return response.text, response.status_code

    def create_user_by_profile(self, profile, login_id, ext=None):
        """Creates the OKTA user

        Arguments:
            firstname {str} -- First Name
            lastname {str} -- Last Name
            login_id {str} -- Login ID, must be unique
            secondary_email {str} -- Email to send initial login information

        Keyword Arguments:
            ext {str} -- Add optional description (default: {None})

        Returns:
            tuple -- returns OKTA id, the user full profile ID, and the status code
        """
        if ext is not None:
            email = f"{login_id}.{ext}@iterable.com"
        else:
            email = f"{login_id}@iterable.com"
        url = self.okta_url + "/api/v1/users?activate=false"
        profile_json = {
            'profile': {
                'email': email,
                'login': email
            }
        }

        for key, value in profile.items():
            profile_json['profile'][key] = value
        print(profile_json)

        response = requests.post(url, headers=self.headers, json=profile_json)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['id'], response_data['profile']['login'], response.status_code

        return None, None, response.status_code