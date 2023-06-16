__author__ = "Rutger Truyers, rtruyers@paloaltonetworks.com"

import os
import requests
import json
import time

def VerifyConfigFile():
    file_path = './prismaaccess/credentials.json'
    if os.path.exists(file_path):
        return (True)
    else:
        return (False)
    
def TAGobject(config_api_endpoint, access_token):
    print("Creating TAG for ADEM ...\n")
    ConfigUrl = f"https://{config_api_endpoint}/sse/config/v1/tags?folder=Shared"
    payload = json.dumps({"color": "Cyan","name": "TEST" })
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.request("POST",ConfigUrl, headers=headers, data=payload)
    if response.status_code == 201:
        print("\033[1;32mCreated Object:ADEM TAG Created: " + "\033[0m \t")
    elif response.status_code == 404:
        error_messages = []
        # Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))
        # Print error messages
        for message in error_messages:
            print("\t"+"\033[1;31m"+ message + ": \033[0m" + "'ADEM' TAG Object\n" )
            
    else:
        print("\t\033[1;31m TAG Creation Failed: " + "\033[0m")
        print ("\tServer Response:" + response.text)

def FQDNobjects(config_api_endpoint, access_token):
    print("Creating FQDN Objects for ADEM ...\n")
    time.sleep(2)
    with open("ademfqdn.txt", "r") as file:
        AdemFQDN = file.read().splitlines()

    ConfigUrl = f"https://{config_api_endpoint}/sse/config/v1/addresses?folder=Shared"
    for i in AdemFQDN:
        payload = json.dumps({"description": "ADEM via API", "name": i, "tag": ["ADEM"], "fqdn": i})
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        response = requests.request("POST", ConfigUrl, headers=headers, data=payload)
        if response.status_code == 201:
            print("\033[1;32m" + "Object Created: " + "\033[0m \t" + i)
        elif response.status_code == 404:
            error_messages = []
            # Extract error messages from 'details'
            for error in response.json().get("_errors"):
                details = error.get('details', {})
                error_messages.append(details.get('message', ''))
            # Print error messages
            for message in error_messages:
                print("\t\033[1;31m"+ message + ": \033[0m" + i )
            
        else:
            print("\n"+"\033[1;31m"+"Object Error:"+ "\033[0m\t" + i)
            print("Response From Server: ")
            print(response.text)



def DynamicAddressGroup(config_api_endpoint, access_token):
    # Creating Dynamic Address Group For ADEM
    ConfigUrl = f"https://{config_api_endpoint}/sse/config/v1/address-groups?folder=Shared"
    payload = json.dumps({"description": "ADEM Group via API", "name": "ADEM", "dynamic": {"filter": "ADEM"}})
    time.sleep(2)
    print("\nCreating a dynamic address Object for adem....\n")
    time.sleep(2)
    # API Request for Dynamic Group Object#
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.request("POST", ConfigUrl, headers=headers, data=payload)

    if response.status_code == 201:
        print("\tADEM Dynamic AddressGroup Creation\t\033[1;32mSuccess\033[0m\n")
    else:
        error_messages = []
        # Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))

        # Print error messages
        for message in error_messages:
            print("\t"+"\033[1;31m"+ message + ": \033[0m" + "ADEM (address group)\n" )


def AdemPreRule(config_api_endpoint, access_token):
    print("Creating ADEM Pre Rule in Shared ... \n")
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
        print("\tAdem PreRule Policy Creation\t\033[1;32m\tSuccess\033[0m\n")
    else:
        error_messages = []
        # Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))

        # Print error messages
        for message in error_messages:
            print("\t" + "\033[1;31m"+ message + ": \033[0m" + "ADEM (PreRule Security Rule in Shared)\n" )



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
    print("\n-------------------------------------")
    print("Script Started")
    print("-------------------------------------\n")
    print("Generating Auth Token ...")
    time.sleep(2)       
    if VerifyConfigFile() == True:
        CONFIG_FILE = "./prismaaccess/credentials.json"
        #read out client credentials
        AUTH_API_ENDPOINT, CONFIG_API_ENDPOINT, TSG_ID, CLIENT_ID, CLIENT_SECRET = getParamFromJson(
            CONFIG_FILE)
        #token generation
        access_token = login_saas(
            AUTH_API_ENDPOINT, TSG_ID, CLIENT_ID, CLIENT_SECRET)
        print ("Auth Token "+ "\033[1;32m" + "\tSucceeded\033[0m\n")
        TAGobject(CONFIG_API_ENDPOINT, access_token)
        FQDNobjects(CONFIG_API_ENDPOINT, access_token)
        DynamicAddressGroup(CONFIG_API_ENDPOINT, access_token)
        AdemPreRule(CONFIG_API_ENDPOINT, access_token)
        print("-------------------------------------")
        print("Script ended succesfully")
        print("-------------------------------------")
    elif VerifyConfigFile() == False:
        print("\nCredentials file \033[1;33m" + "./prismaaccess/credentials.json" +"\033[0m is"+"\033[1;31m missing" + "\033[0m, \nThis is Required for Authentication")
        print("Pleae refer to readme document on github for instructions")
        print("-------------------------------------")
        print("Script ended with \033[1;31m" + "issues"+ "\033[0m")
        print("-------------------------------------")

#os.environ['HOME'] + 

if __name__ == "__main__":
    main()


