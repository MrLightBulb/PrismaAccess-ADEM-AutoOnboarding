import os
import requests
import json
import time

client_id = ''
client_secret = ''
tsg_id = ''
VerifyAuthResult = ''
TokenResult = ''
access_token = ''


def verifyauth():
    # Check if the file exists
    global client_id
    global client_secret
    global tsg_id
    print("")
    print ("Start auth Verification..... ")
    file_path = "./auth.txt"
    time.sleep(2)
    if not os.path.isfile(file_path):
        return ("noauth");
    else:
        # Get the file's modification time
        file_modified_time = os.path.getmtime(file_path)
        
        # Get the current time
        current_time = time.time()
        
        # Calculate the time difference in minutes
        time_difference_minutes = (current_time - file_modified_time) / 60
        
        # Check if the file is older than 15 minutes
        if time_difference_minutes > 15:
            # Delete the file
            os.remove(file_path)
            return ("expired")
        else:
            #  Read the contents of the file
            with open(file_path, "r") as file:
                lines = file.readlines()
                
            # Check if the file contains the expected number of lines
            if len(lines) < 3:
                print("Invalid Auth File")
                return ("noauth")
            else:
                # Read the contents of the file
                print("Found Auth File")
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    #Extract the values from the lines
                    client_id = lines[0].strip()
                    client_secret = lines[1].strip()
                    tsg_id = lines[2].strip()
                return ("success")

def Authentication():
    print("")
    print ("fill in the Access information in below prompts ")
    global client_id
    global client_secret
    global tsg_id
    client_id = input("Enter yoour client-id: ")
    client_secret = input ("Enter your client-secret: ")
    tsg_id = input("Enter TSG ID of your tenant: ")
    WriteToAuthFile()

def TokenGeneration():
    global client_id
    global client_secret
    global tsg_id
    global access_token
    print("")
    print("Generating Token .... ")
    print("values in tokengenerator:")
    print("id  ", client_id,"secret ", client_secret, " tsg ", tsg_id) 
    AccessUrl = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
    data = {"grant_type": "client_credentials","scope": f"tsg_id:{tsg_id}"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(AccessUrl, data=data, headers=headers, auth=(client_id, client_secret))

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("-------------------------------------")
        print("Generating Access Token ...")
        time.sleep(2)
        print("One Time Access Token Succesfully Generated")
        time.sleep(2)
        return("success")
    else:
        print("!!! One Time Access Token Geration Failed !!!")
        return("fail")
    
def WriteToAuthFile():
    global client_id
    global client_secret
    global tsg_id
    print("values in write to file:")
    print("id  ", client_id,"secret ", client_secret, " tsg ", tsg_id) 
    file_path = "./auth.txt"

    # Create the file
    open(file_path, "w").close()

    # Open the file in write mode and write the values
    with open(file_path, "w") as file:
        # Write the values to the file, each on a new line
        file.write(client_id + "\n")
        file.write(client_secret + "\n")
        file.write(tsg_id + "\n")
        print("Values written to the file:", file_path)

def FQDNobjects():
    print("-------------------------------------")
    print("Creating FQDN Objects for ADEM ... ")
    time.sleep(2)
    print("")
    with open('ademfqdn.txt', 'r') as file: 
        AdemFQDN = file.read().splitlines()
    ConfigUrl = "https://api.sase.paloaltonetworks.com/sse/config/v1/addresses?folder=Shared"
    for i in AdemFQDN:
        payload = json.dumps({
        "description": "ADEM via API",
        "name": i,
        "tag": ["ADEM"],
        "fqdn": i
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
        response = requests.request("POST", ConfigUrl, headers=headers, data=payload)
        if response.status_code == 201:
            print(i,"Created OK")
        else:
            print("")
            print("!!! ADEM FQDN OBject",i, "Creation Error !!!")
            print("Response From Server: ")
            print(response.text)
            print("")

def DynamicAddressGroup():
    #Creating Dynamic Address Group For ADEM
    ConfigUrl = "https://api.sase.paloaltonetworks.com/sse/config/v1/address-groups?folder=Shared"
    payload = json.dumps({
    "description": "ADEM Group via API",
    "name": "ADEM",
        "dynamic": {
            "filter":"ADEM"
        }
    })
    time.sleep(2)
    print("")
    print("-------------------------------------")
    print("Creating a dynamic address ojbect for adem....")
    print("")
    time.sleep(2)
    #API Request for Dynamic Group Object#
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("POST", ConfigUrl, headers=headers, data=payload)

    if response.status_code == 201:
        print("ADEM Dynamic AddressGroup Succesfully Created")
        print("")
    else:
        print("ADEM Dynamic AddressGroup Error")
        print("Response Error:", response.status_code)
        print("Response Details", response.text)

def AdemPreRule():
    print("-------------------------------------")
    print("Creating ADEM Pre Rule in Shared ... ")
    time.sleep(2)
    PolicyUrl = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules?position=pre&folder=Shared"
    payload = json.dumps({
        "name": "ADEM",
        "description": "ADEM Service",
        "action": "allow",
        "application": [
            "any"
        ],
        "from": [
            "trust"
        ],
        "source": [
            "any"
        ],
        "source_user": [
            "any"
        ],
        "to": [
            "untrust"
        ],
        "destination": [
            "ADEM"
        ],
        "service": [
            "any"
        ],
        "category": [
            "any"
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
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

def Script():
    AccessResponse = ""
    print("")
    print("-------------------------------------")
    print ("Start ADEM Onboarding Script ")
    print("-------------------------------------")
    VerifyAuthResult = verifyauth()
    if VerifyAuthResult == "success":
            TokenResult = TokenGeneration()
            if TokenResult == "success":
                FQDNobjects()
                DynamicAddressGroup()
                AdemPreRule()
                print("-------------------------------------")
                print ("Script ended Succesfully")
                print("-------------------------------------")
            else:
                print("")
                print("Generating Token Failed")
                print("-------------------------------------")
                print ("Script ended with issues")
                print("-------------------------------------")
    if VerifyAuthResult == "noauth":
        print("")
        print("No Existing Authentication")
        print("")
        print("Starting Authenitcation process ...")
        time.sleep(3)
        Authentication()
        TokenResult = TokenGeneration()
        if TokenResult == "success":
            FQDNobjects()
            DynamicAddressGroup()
            AdemPreRule()
            print("-------------------------------------")
            print ("Script ended succesfully")
            print("-------------------------------------")
        if TokenResult == "fail":
            print("")
            print("!! Token failed, Pleae try again !!")
            print("")
            print("-------------------------------------")
            print ("Script ended with issues")
            print("-------------------------------------")

        time.sleep(2)
    if VerifyAuthResult == "expired":
        print("")
        print("Token expired")
        print("Restarting authentication proces...")
        time.sleep(2)
        if AccessResponse == "success":
            FQDNobjects()
            DynamicAddressGroup()
            AdemPreRule()
            print("-------------------------------------")
            print ("Script ended succesfully")
            print("-------------------------------------")
        if AccessResponse == "fail":
            print("")
            print("!! Authentication failed, Please verify credentials !!")
            print("")
            print("-------------------------------------")
            print ("Script ended with issues")
            print("-------------------------------------")
    
Script()