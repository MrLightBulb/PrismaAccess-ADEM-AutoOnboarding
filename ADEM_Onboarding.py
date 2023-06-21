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
    
def TAGobject(Config_Url, BearerToken):
    print("Creating TAG for ADEM ...\n")
    ConfigUrl = f"https://{Config_Url}/sse/config/v1/tags?folder=Shared"
    payload = json.dumps({"color": "Cyan","name": "ADEM" })
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
    response = requests.request("POST",ConfigUrl, headers=headers, data=payload)
    if response.status_code == 201:
        print("\t\033[1;32mTag Object Created:\033[0m\tADEM\n")
    elif response.status_code == 404:
        error_messages = []
        # Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))
        # Print error messages
        for message in error_messages:
            print("\t\033[1;31mTAG Object "+ message +":\033[0m"+" ADEM\n")
            
    else:
        print("\t\033[1;31m TAG Object Creation Failed: " + "\033[0m")
        print ("\tServer Response:" + response.text)

def FQDNobjects(Config_Url, BearerToken):
    print("Creating FQDN Objects for ADEM ...\n")
    time.sleep(2)
    with open("ademfqdn.txt", "r") as file:
        AdemFQDN = file.read().splitlines()

    ConfigUrl = f"https://{Config_Url}/sse/config/v1/addresses?folder=Shared"
    for i in AdemFQDN:
        payload = json.dumps({"description": "ADEM via API", "name": i, "tag": ["ADEM"], "fqdn": i})
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
        response = requests.request("POST", ConfigUrl, headers=headers, data=payload)
        if response.status_code == 201:
            print("\t\033[1;32m" + "FQDN Object Created: " + "\033[0m \t" + i)
        elif response.status_code == 404:
            error_messages = []
            # Extract error messages from 'details'
            for error in response.json().get("_errors"):
                details = error.get('details', {})
                error_messages.append(details.get('message', ''))
            # Print error messages
            for message in error_messages:
                print("\t\033[1;31mFQDN "+ message + ": \033[0m" + i )
            
        else:
            print("\n"+"\033[1;31m"+"Object Error:"+ "\033[0m\t" + i)
            print("Response From Server: ")
            print(response.text)



def DynamicAddressGroup(Config_Url, BearerToken):
    # Creating Dynamic Address Group For ADEM
    ConfigUrl = f"https://{Config_Url}/sse/config/v1/address-groups?folder=Shared"
    payload = json.dumps({"description": "ADEM Group via API", "name": "ADEM", "dynamic": {"filter": "ADEM"}})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
    response = requests.request("POST", ConfigUrl, headers=headers, data=payload)
    time.sleep(2)
    print("\nCreating a dynamic address Object for adem....\n")
    time.sleep(2)
    # API Request for Dynamic Group Object#
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
            print("\t"+"\033[1;31mDynamic AddressGroup "+ message + ": \033[0mADEM\n" )


def AdemPreRule(Config_Url, BearerToken):
    print("Creating ADEM Pre Rule in Shared ... \n")
    time.sleep(2)
    PolicyUrl = f"https://{Config_Url}/sse/config/v1/security-rules?position=pre&folder=Shared"
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
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
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
            print("\t" + "\033[1;31mShared PreRule "+ message + ": \033[0m" + "ADEM\n" )

def DecryptProfile(Config_Url, BearerToken):
    print("Creating ADEM Decryption Profile in Shared ... \n")
    time.sleep(2)
    DecryptProfileUrl = f"https://{Config_Url}/sse/config/v1/decryption-profiles?folder=Shared"
    payload = json.dumps({
    "name": "ADEM_DecryptProfile",
    "ssl_forward_proxy": {
        "auto_include_altname": False,
        "block_client_cert": False,
        "block_expired_certificate": True,
        "block_timeout_cert": False,
        "block_tls13_downgrade_no_resource": False,
        "block_unknown_cert": False,
        "block_unsupported_cipher": False,
        "block_unsupported_version": False,
        "block_untrusted_issuer": False,
        "restrict_cert_exts": False,
        "strip_alpn": False
    },
    "ssl_no_proxy": {
        "block_expired_certificate": True,
        "block_untrusted_issuer": False
    },
    "ssl_protocol_settings": {
        "auth_algo_md5": True,
        "auth_algo_sha1": True,
        "auth_algo_sha256": True,
        "auth_algo_sha384": True,
        "enc_algo_3des": True,
        "enc_algo_aes_128_cbc": True,
        "enc_algo_aes_128_gcm": True,
        "enc_algo_aes_256_cbc": True,
        "enc_algo_aes_256_gcm": True,
        "enc_algo_chacha20_poly1305": True,
        "enc_algo_rc4": True,
        "keyxchg_algo_dhe": True,
        "keyxchg_algo_ecdhe": True,
        "keyxchg_algo_rsa": True,
        "max_version": "max",
        "min_version": "tls1-0"
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <TOKEN>'
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
    response = requests.request("POST", DecryptProfileUrl, headers=headers, data=payload)
    if response.status_code == 201:
        print("\tADEM Decrypt Profile Creation\t\033[1;32m\tSuccess\033[0m\n")
    else:
        error_messages = []
        
        #Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))

        #Print error messages
        for message in error_messages:
            print("\t" + "\033[1;31mDecrypt Profile "+ message + ": \033[0m" + "ADEM_DecryptProfile\n" )


def DecryptRule(Config_Url, BearerToken):
    print("Creating \"ADEM NoDecrypt\" Decryption Rule in Shared ... \n")
    time.sleep(2)
    DecryptUrl = f"https://{Config_Url}/sse/config/v1/decryption-rules?position=pre&folder=Shared"
    payload = json.dumps({
        "name": "ADEM - NoDecrypt",
        "action": "no-decrypt",
        "description": "ADEM No Decrypt Rule",
        "source": [
            "any"
        ],
        "source_user": [
            "any"
        ],
        "from": [
            "trust"
        ],
        "destination": [
            "ADEM"
        ],
        "to": [
            "untrust"
        ],
        "category": [
            "any"
        ],
        "service": [
            "any"
        ],
        "disabled": False,
        "log_fail": True,
        "log_success": True,
        "profile": "ADEM_DecryptProfile",
        "tag": [
            "ADEM"
        ],
        "type": {
            "ssl_forward_proxy": {}
        }
    })
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
    response = requests.request("POST", DecryptUrl, headers=headers, data=payload)
    if response.status_code == 201:
        print("\tADEM No Decrypt Rule Creation\t\033[1;32m\tSuccess\033[0m\n")
    else:
        error_messages = []

        #Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))

        # Print error messages
        for message in error_messages:
            print("\t" + "\033[1;31mDecryption Rule "+ message + ": \033[0m" + "ADEM NoDecrypt\n" )


def getBearerToken(auth_url, tsg_id, client_id, client_secret):
    url = f"https://{auth_url}/oauth2/access_token"
    #Setting API Payload to be send
    payload = {
        "grant_type": "client_credentials",
        "scope": f"tsg_id:{tsg_id}"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    #captering Response from API Request
    response = requests.post(url, data=payload,headers=headers, auth=(client_id, client_secret))
    #Reteruning BearerToken
    return response.json().get("access_token")

def getParamFromJson(config_file):
    f = open(config_file,)
    params = json.load(f)
    Auth_Url = params["Auth_Url"]
    Config_Url = params["Config_Url"]
    tsg_id = params["tsg_id"]
    client_id = params["client_id"]
    client_secret = params["client_secret"]
    # Closing file
    f.close()
    return Auth_Url, Config_Url, tsg_id, client_id, client_secret

def commitstatus():
    print ("verifying commit status")

def commit(BearerToken):
    # Sending Candidate to be commited 
    CommitUrl = f"https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/candidate:push"
    # Setting API Payload values
    payload = json.dumps ({
        "description": "ADEM API Script",
        "folders": ["Mobile Users", "Remote Networks", "Service Connections"],
    })
    #Defining the API Headers
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BearerToken}"}
    #capturing response from api server
    response = requests.request("POST", CommitUrl, headers=headers, data=payload)
    if response.status_code == 200:
        print("\tCommit Changes\t\033[1;32m\tInitiated\033[0m")
        time.sleep(2)
        # Find the JSON portion of the Commit Job ID and Print
        json_start = response.text.find('{')
        json_end = response.text.rfind('}')
        json_data = response.text[json_start : json_end + 1]
        response_data = json.loads(json_data)
        commit_job = response_data["message"]
        print("\t\033[1;33m" + commit_job + "\033[0m\n")
    else:
        print ("response message:")
        print(response.text + "\n")
        error_messages = []
        # Extract error messages from 'details'
        for error in response.json().get("_errors"):
            details = error.get('details', {})
            error_messages.append(details.get('message', ''))

        # Print error messages
        for message in error_messages:
            print("\tCommit Changes Initiation \033[1;31mFailed\033[0m)" )
            print("\tReason:\t" + "\033[1;31m"+ message + ": \033[0m")


def AskCommit():
    prompt = 'Do you want to commit these changes ? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is \033[1;31mInvalid \033[0m, please try again...\n')
        return AskCommit()
    if ans in ['y','Y','yes','Yes','YES']:
        return True
    if ans in ['n','N','no','No','NO']:
        return False
    else:
        print(f'{ans} is \033[1;31mInvalid \033[0m, please try again...\n')
        return AskCommit()

def main():
    print("\n-------------------------------------")
    print("Script Started")
    print("-------------------------------------\n")
    print("Generating Auth Token ...\n")
    time.sleep(2)       
    if VerifyConfigFile() == True:
        CONFIG_FILE = "./prismaaccess/credentials.json"
        #read out client credentials
        Auth_Url, Config_Url, TSG_ID, CLIENT_ID, CLIENT_SECRET = getParamFromJson(CONFIG_FILE)
        #token generation
        BearerToken = getBearerToken(Auth_Url, TSG_ID, CLIENT_ID, CLIENT_SECRET)
        print ("\tAuth Token Generation"+ "\033[1;32m" + "\tSucceeded\033[0m\n")
        TAGobject(Config_Url, BearerToken)
        FQDNobjects(Config_Url, BearerToken)
        DynamicAddressGroup(Config_Url, BearerToken)
        AdemPreRule(Config_Url, BearerToken)
        DecryptProfile(Config_Url,BearerToken)
        DecryptRule(Config_Url, BearerToken)
        CommitConfirm = AskCommit()
        if CommitConfirm == True:
            commit(BearerToken)
        elif CommitConfirm == False:
            print ("\n\tChanges \033[1;32mSaved \033[0m, Changes \033[1;31mNOT Commited\033[0m")
        print("\n-------------------------------------")
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


