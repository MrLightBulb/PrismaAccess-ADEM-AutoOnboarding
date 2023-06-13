import requests
import json
import time

AccessUrl = "https://auth.apps.paloaltonetworks.com/oauth2/access_token"
client_id = "beluxapi@1530061237.iam.panserviceaccount.com"
client_secret = "369b22be-dc0a-4473-958b-d12018fb98f9"
tsg_id = "1530061237"

data = {
    "grant_type": "client_credentials",
    "scope": f"tsg_id:{tsg_id}"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(AccessUrl, data=data, headers=headers, auth=(client_id, client_secret))

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("-------------------------------------")
    print("Generating Access Token ...")
    time.sleep(2)
    print("One Time Access Token Succesfully Generated")
    time.sleep(2)
else:
    print("Error:", response.text)
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

#SecurityPolicy

print("-------------------------------------")
print("Creating ADEM Pre Rule in Shared ... ")
time.sleep(2)

PolicyUrl = "https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules?position=pre&folder=Shared"

payload = json.dumps({
    "name": "ADEM via API",
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