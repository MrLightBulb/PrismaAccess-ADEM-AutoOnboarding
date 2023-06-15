__author__ = "Rutger Truyers"

import os
import requests
import json
import time


def FQDNobjects(config_api_endpoint, access_token):
    print("-------------------------------------")
    print("Creating FQDN Objects for ADEM ... ")
    time.sleep(2)
    print("")

    with open("ademfqdn.txt", "r") as file:
        AdemFQDN = file.read().splitlines()

    ConfigUrl = f"https://{config_api_endpoint}/sse/config/v1/addresses?folder=Shared"
    for i in AdemFQDN:
        payload = json.dumps({"description": "ADEM via API", "name": i, "tag": ["ADEM"], "fqdn": i})
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        response = requests.request("POST", ConfigUrl, headers=headers, data=payload)
        print(response.status_code)
        if response.status_code == 201:
            print(i, "Created OK")
        elif response.status_code == 404:
            print("")
            print("!!! TEST ADEM FQDN OBject", i, "Creation Error !!!")
            print("Response From Server: ")

            error_messages = []
            # Extract error messages from 'details'
            for error in response.json().get("_errors"):
                details = error.get('details', {})
                error_messages.append(details.get('message', ''))

            # Print error messages
            for message in error_messages:
                print(message)
                
            print("")
            
        else:
            print("")
            print("!!! ADEM FQDN OBject", i, "Creation Error !!!")
            print("Response From Server: ")
            print(response.text)
            print("")


def DynamicAddressGroup(config_api_endpoint, access_token):
    # Creating Dynamic Address Group For ADEM
    ConfigUrl = f"https://{config_api_endpoint}/sse/config/v1/address-groups?folder=Shared"
    payload = json.dumps({"description": "ADEM Group via API", "name": "ADEM", "dynamic": {"filter": "ADEM"}})
    time.sleep(2)
    print("")
    print("-------------------------------------")
    print("Creating a dynamic address ojbect for adem....")
    print("")
    time.sleep(2)
    # API Request for Dynamic Group Object#
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.request("POST", ConfigUrl, headers=headers, data=payload)

    if response.status_code == 201:
        print("ADEM Dynamic AddressGroup Succesfully Created")
        print("")
    else:
        print("ADEM Dynamic AddressGroup Error")
        print("Response Error:", response.status_code)
        print("Response Details", response.text)


def AdemPreRule(config_api_endpoint, access_token):
    print("-------------------------------------")
    print("Creating ADEM Pre Rule in Shared ... ")
    time.sleep(2)
    PolicyUrl = f"https://{config_api_endpoint}/sse/config/v1/security-rules?position=pre&folder=Shared"
    payload = json.dumps(
        {
            "name": "ADEM",
            "description": "ADEM Service",
            "action": "allow",
            "application": ["any"],
            "from": ["trust"],
            "source": ["any"],
            "source_user": ["any"],
            "to": ["untrust"],
            "destination": ["ADEM"],
            "service": ["any"],
            "category": ["any"],
        }
    )
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.request("POST", PolicyUrl, headers=headers, data=payload)
    if response.status_code == 201:
        print("")
        print("PreRule Policy Created Successfully")
        print("")
    else:
        print("")
        print("PreRule Policy Created Failed")
        print("Response Error:", response.status_code)
        print("Response Details", response.text)



def login_saas(base_url, tsg_id, client_id, client_secret):
    url = f"https://{base_url}/oauth2/access_token"

    payload = {
        "grant_type": "client_credentials",
        "scope": f"tsg_id:{tsg_id}"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload,
                             headers=headers, auth=(client_id, client_secret))
    
    return response.json().get("access_token")

def getParamFromJson(config_file):
    f = open(config_file,)
    params = json.load(f)
    auth_api_endpoint = params["auth_api_endpoint"]
    config_api_endpoint = params["config_api_endpoint"]
    tsg_id = params["tsg_id"]
    client_id = params["client_id"]
    client_secret = params["client_secret"]
    # Closing file
    f.close()
    return auth_api_endpoint, config_api_endpoint, tsg_id, client_id, client_secret


def main():
    CONFIG_FILE = os.environ['HOME'] + "/.prismaaccess/credentials.json"
    AUTH_API_ENDPOINT, CONFIG_API_ENDPOINT, TSG_ID, CLIENT_ID, CLIENT_SECRET = getParamFromJson(
        CONFIG_FILE)
    access_token = login_saas(
        AUTH_API_ENDPOINT, TSG_ID, CLIENT_ID, CLIENT_SECRET)
    
    FQDNobjects(CONFIG_API_ENDPOINT, access_token)
    DynamicAddressGroup(CONFIG_API_ENDPOINT, access_token)
    AdemPreRule(CONFIG_API_ENDPOINT, access_token)
    print("-------------------------------------")
    print("Script ended succesfully")
    print("-------------------------------------")


if __name__ == "__main__":
    main()


