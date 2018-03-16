# Name:        roxe.py
# Author:      sebastien.ehrhard@al-enterprise.com
# Created:     14/12/2017
# Copyright:   (c) sehrhard 2018
#
# This example connects to the ROXE and save into a file all the users logins, passwords, company phone numbers, first and last names, voice mail, devices list, API rights, OXE node id, supported and GUI language
#
# ToDo
#

import json
import requests
import csv
import sys


# the user class
class User:

    def __init__(self, login="", password=""):

        voice_mail = Voicemail()
        user_preferences = UserPreferences()
        supported_languages = SupportedLanguages()

        self.login = login
        self.password = password
        self.companyPhone = ""
        self.firstName = ""
        self.lastName = ""
        self.voicemail = voice_mail
        self.devices = []
        self.apiRights = []
        self.nodeId = ""
        self.user_preferences = user_preferences
        self.supported_languages = supported_languages

    # get the user information
    def get(self):
        return [self.login, self.password, self.companyPhone, self.firstName, self.lastName, self.get_voicemail(), self.get_devices(), self.get_api_rights(), self.nodeId, self.user_preferences.get(), self.supported_languages.get()]

    # get the devices list information
    def get_devices(self):
        return_value = ""
        for one_device in self.devices:
            return_value += one_device.type + " " + one_device.id + " " + one_device.subType + "\n"
        # remove last line return
        if len(return_value):
            return_value = return_value[:-1]
        return return_value

    # get the API rights information
    def get_api_rights(self):
        return_value = ""
        for one_right in self.apiRights:
            return_value += one_right + "\n"
        # remove last line return
        if len(return_value):
            return_value = return_value[:-1]
        return return_value

    # get the voice mail information
    def get_voicemail(self):
        return self.voicemail.number + "\n" + self.voicemail.type

    # get the information header
    def get_header(self):
        return ["login", "password", "company phone", "first name", "last name", "voice mail", "devices", "API rights", "node ID", "GUI language", "Supported languages"]


# the voice mail class
class Voicemail:

    def __init__(self, number="", type=""):
        self.type = type
        self.number = number

    def get(self):
        return [self.number, self.type]


# the device class
class Device:

    def __init__(self, type="", id="", sub_type=""):
        self.type = type
        self.id = id
        self.subType = sub_type

    # get the device information
    def get(self):
        return [self.type, self.id, self.subType]


# the users preferences class
class UserPreferences:

    def __init__(self, gui_language=""):
        self.guiLanguage = gui_language

    def get(self):
        return self.guiLanguage


# the users supported languages class
class SupportedLanguages:

    def __init__(self, supported_languages=[]):
        self.SupportedLanguages = supported_languages

    def get(self):
        return_value = ""
        for one_language in self.SupportedLanguages:
            return_value += one_language + "\n"
        # remove last line return
        if len(return_value):
            return_value = return_value[:-1]
        return return_value


# the authentication answer class
class AuthAnswer:

    def __init__(self):
        self.credential = ""
        self.publicUrl = ""
        self.internalUrl = ""
        self.session_url = ""


# the session class
class Session:

    def __init__(self, url, user, cookie, app_name):
        self.url = url
        self.user = user
        self.cookie = cookie
        self.app_name = app_name


# the session information class
class SessionInfo:

    def __init__(self):
        self.admin = False
        self.timeToLive = 0
        self.publicBaseUrl = ""
        self.privateBaseUrl = ""
        self.base_url = ""
        self.cookie = ""


# the ROXE class
class Roxe:

    # the method labels
    METHOD_GET = "GET"
    METHOD_PUT = "PUT"
    METHOD_POST = "POST"
    METHOD_DELETE = "DELETE"

    def __init__(self, host='', port=0, use_internal_access=True, debug_mode=False):
        self.host = host
        if port == 0:
            self.port = 443  # https default port
            self.base_url = "https://" + self.host
        else:
            self.port = port
            self.base_url = "https://" + self.host + ":" + str(port)

        self.publicUrl = ""
        self.internalUrl = ""
        self.headers = {'Content-type': 'application/json'}
        self.use_internal_access = use_internal_access
        self.authentication_url = ""
        self.debug_mode = debug_mode

        return

    # the HTTP generic method
    def call(self, cookie, method, url, data={}):

        data_json = json.dumps(data)

        try:

            if method == self.METHOD_GET:
                response = requests.get(url, data=data_json, cookies=cookie, headers=self.headers, verify=False)
            elif method == self.METHOD_PUT:
                response = requests.put(url, data=data_json, cookies=cookie, headers=self.headers, verify=False)
            elif method == self.METHOD_POST:
                response = requests.post(url, data=data_json, cookies=cookie, headers=self.headers, verify=False)
            elif method == self.METHOD_DELETE:
                response = requests.delete(url, data=data_json, cookies=cookie, headers=self.headers, verify=False)

            else:
                response = ''

            if self.debug_mode:
                print(method)
                print(url)
                print(data_json)
                print
                print(response.status_code)
                print(response.text)
                print
                print

            return response

        except:

            print("Error with method " + method)
            print(url)
            print (data_json)
            print
            return ''

    # the GET method
    def get(self, cookie, url, data={}):

        return self.call(cookie, self.METHOD_GET, url, data)

    # the PUT method
    def put(self, cookie, url, data={}):

        return self.call(cookie, self.METHOD_PUT, url, data)

    # the POST method
    def post(self, cookie, url, data={}):

        return self.call(cookie, self.METHOD_POST, url, data)

    # the DELETE method
    def delete(self, cookie, url, data={}):

        return self.call(cookie, self.METHOD_DELETE, url, data)

    # connect to the ROXE and get the basic information
    def get_basic_info(self):

        try:

            response = self.get("", self.base_url + "/api/rest")

            # if method is succesfull
            if response.status_code == 200:
                json_response = json.loads(response.text)
                # get the public URL
                self.publicUrl = json_response["versions"][0]["publicUrl"]
                # get the internal (private) URL
                self.internalUrl = json_response["versions"][0]["internalUrl"]

                # depending on the chosen configuration, store the authentication URL
                if self.use_internal_access:
                    self.authentication_url = self.internalUrl
                else:
                    self.authentication_url = self.publicUrl

                return response

            return ""

        except:

            return ""

    # authenticate
    def authenticate(self, user):

        auth_response = AuthAnswer()

        try:

            response = requests.get(self.authentication_url, auth=requests.auth.HTTPBasicAuth(user.login, user.password), headers=self.headers, verify=False)

            # if authentication is successful
            if response.status_code == 200:

                json_response = json.loads(response.text)
                # get the credentials
                auth_response.credential = json_response["credential"]
                # get the public URL
                auth_response.publicUrl = json_response["publicUrl"]
                # get the private (internal) URL
                auth_response.internalUrl = json_response["internalUrl"]

                # depending on the chosen configuration, store the session URL
                if self.use_internal_access:
                    auth_response.session_url = auth_response.internalUrl
                else:
                    auth_response.session_url = auth_response.publicUrl

            if self.debug_mode:
                print(self.METHOD_GET)
                print(self.authentication_url)
                print(response.status_code)
                print(response.text)
                print

            return auth_response

        except:

            print("Error with authentication")
            print(self.authentication_url)
            print('')
            return auth_response

    # open a session
    def open_session(self, session):

        session_info_response = SessionInfo()

        data = {"applicationName":session.app_name}

        try:

            response = self.post(session.cookie, session.url, data)

            if self.debug_mode:
                print(self.METHOD_POST)
                print(session.url)
                print(data)
                print(response.status_code)
                print(response.text)
                print

            # if method is successful
            if response.status_code == 200:
                json_response = json.loads(response.text)
                # get the session information
                session_info_response.admin = json_response["admin"]
                session_info_response.timeToLive = json_response["timeToLive"]
                session_info_response.publicBaseUrl = json_response["publicBaseUrl"]
                session_info_response.privateBaseUrl = json_response["privateBaseUrl"]
                # depending on the chosen configuration, store the base URL
                if self.use_internal_access:
                    session_info_response.base_url = session_info_response.privateBaseUrl
                else:
                    session_info_response.base_url = session_info_response.publicBaseUrl
                session_info_response.cookie = session.cookie

                return session_info_response

        except:

            print("Error with session opening")
            print(session.url)
            print('')
            return session_info_response

    # close a session
    def close_session(self, session):

        return self.delete(session.cookie, session.url)


# the REST API example class
class RestApi:

    def __init__(self, roxe):
        # the ROXE object
        self.roxe = roxe
        # the user used to authenticate and open a session
        self.user = None
        # the session object
        self.session = Session("", None, "", "")
        # the sessions information object
        self.session_info = SessionInfo()
        # the list of the user logins
        self.logins = []
        # the list of the users
        self.users = {}
        # the list of the pbxs nodeIds
        self.nodeIds = []

        return

    # get the ROXE information, authenticate, open a session and get the user logins list
    def start(self, user):

        self.user = user

        # get the ROXE instance information
        self.roxe.get_basic_info()

        # create empty authentication answer
        auth_answer = AuthAnswer()

        # authenticate
        auth_answer = self.roxe.authenticate(self.user)

        # create the session instance
        self.session = Session(auth_answer.session_url, self.user, dict(AlcUserId=auth_answer.credential), "Sebastien")

        # open the session
        self.session_info = self.roxe.open_session(self.session)

        # get all the user logins
        return self.get_user_logins()

    # close the session
    def stop(self):
        return self.roxe.close_session(self.session)

    # get the user logins list
    def get_user_logins(self):

        response = self.roxe.get(self.session_info.cookie, self.session_info.base_url + "/logins")
        if response and response.status_code == 200:
            json_response = json.loads(response.text)
            self.logins = json_response["loginNames"]
            self.get_users_info()

        return self.logins

    # get the users information
    def get_users_info(self):

        self.users = {}
        for one_login in self.logins:
            self.users[one_login] = self.get_user_info(one_login)
            self.users[one_login].user_preferences = self.get_user_preferences(one_login)
            self.users[one_login].supported_languages = self.get_supported_languages(one_login)

        return self.users

    # get one user information
    def get_user_info(self, login_name):

        response = self.roxe.get(self.session_info.cookie, self.session_info.base_url + "/users/" + login_name)
        if response.status_code == 200:
            user = User()
            json_response = json.loads(response.text)
            if "loginName" in json_response:
                user.login = json_response["loginName"]
            if "firstName" in json_response:
                user.firstName = json_response["firstName"]
            if "lastName" in json_response:
                user.lastName = json_response["lastName"]
            if "companyPhone" in json_response:
                user.companyPhone = json_response["companyPhone"]
            user.voicemail = Voicemail()
            if "voicemail" in json_response:
                user.voicemail = Voicemail(json_response["voicemail"]["number"], json_response["voicemail"]["id"])

            user.devices = []
            if "devices" in json_response:
                for one_device in json_response["devices"]:
                    device = Device(one_device["type"], one_device["id"], one_device["subType"])
                    user.devices.append(device)
            if "apiRights" in json_response:
                user.apiRights = json_response["apiRights"]
            if "nodeId" in json_response:
                user.nodeId = json_response["nodeId"]

            return user

        return User()

    # get one user preferences
    def get_user_preferences(self, login_name):

        user_preferences = UserPreferences()

        response = self.roxe.get(self.session_info.cookie, self.session_info.base_url + "/users/" + login_name + "/preferences")
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if "guiLanguage" in json_response:
                user_preferences.guiLanguage = json_response["guiLanguage"]

        return user_preferences

    # get one user supported languages
    def get_supported_languages(self, login_name):

        supported_languages = []

        response = self.roxe.get(self.session_info.cookie, self.session_info.base_url + "/users/" + login_name + "/preferences/supportedLanguages")
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if "supportedLanguages" in json_response:
                for one_language in json_response["supportedLanguages"]:
                    supported_languages.append(one_language)

        return SupportedLanguages(supported_languages)


def main():

    # check if admin login and password have been given as arguments
    if len(sys.argv) != 7:
        print("Missing ROXE FQDN, ROXE port, admin login, password, private or public access and debug mode in arguments")
        return

    # create ROXE instance with the arguments
    roxe = Roxe(sys.argv[1], sys.argv[2], sys.argv[5] == "True", sys.argv[6] == "True")

    # create the user instance with login and password (given as arguments)
    user = User(sys.argv[3], sys.argv[4])

    # create RestApi instance
    restapi = RestApi(roxe)

    # connect, authenticate, open a session and get the users logins
    restapi.start(user)

    # for each user, save his information into user.csv file
    with open("user.csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n', delimiter=';')
        # write the column labels
        writer.writerow(User().get_header())

        for one_login in restapi.logins:
            writer.writerow(restapi.users[one_login].get())

    return

main()