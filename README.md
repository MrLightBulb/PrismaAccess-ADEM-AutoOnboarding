# PrismaAccess-ADEM-AutoOnboarding
When onboarding ADEM you have to create all the FQDN Objects and Policy as described in [this palo alto networks doc](https://docs.paloaltonetworks.com/autonomous-dem/autonomous-dem-admin/get-started-with-adem/enable-adem-for-mobile-users/enable-adem-in-cloud-managed-pa-mu#enable-autonomous-dem-in-cloud-managed-prisma-access)

# Prerequisites

Define a Prisma Access Tenant `Service Account`, here is a [howto](https://docs.paloaltonetworks.com/common-services/identity-and-access-access-management/manage-identity-and-access/add-service-accounts)

This service account is required in order to create an access token to use the API infrastructure of your Prisma Acces Tenant

Create a file into home directory `.prismaaccess/credentials.json` with the following structure:

```json
{
    "Auth_Url": "auth.apps.paloaltonetworks.com",
    "Config_Url": "api.sase.paloaltonetworks.com",
    "tsg_id": "<Your-TSG-ID>",
    "client_id": "<Your-Client-ID>",
    "client_secret": "<Your-Client-Secret>"
}
```

# What it can do

- This only works for Prisma Access Cloud Management
- Auto Generate all required ADEM FQDN objects under Shared Level
- Auto Generate a Dynamic Address group that consists all the ADEM FQDN objects
- Auto Generate a Pre-Rule Policy to allow traffic towards the ADEM FQND Service Objects

# What it cannot do

- Commit the changes, it will only generate a config candidate, this means you still need to perform a commit in the interface
- Choosing a name convention for your objects.
- Changing the Global protect App settings to auto enable the ADEM Configuration.
- Support for Panorama

# Short term Roadmap:

- Auto Commit changes after user input 
- Adding naming convetion

# Long Term Roadmap:

- changing the global app settings with ADEM Config 
due to missing API calls this is currently not possible, waiting for new API tools for Global Protect.

# How It Works
This script is leveraging the Prisma Access Cloud Mgmt API infrastructure.<br>
In order to leverage the API calls we need to create a Bearer Token to perform the calls.<br>
The bearor token is generated from the Tenant Service Account information,<br>which you need to provide in the '/.prismaaccess/credentials.json' file<br>

More information how it works can be found in the official Palo Alto Networks documentations:
- Prisma Access Tenant Service Account [documentation](https://pan.dev/sase/docs/getstarted/)
- Bearer token [documentation](https://pan.dev/sase/docs/access-tokens/)

A bearor token is valid for 15min.<br>
Each time you run the script a new unique bearor token is generated.<br>

# How to use
when the github respoistory has been downloaded launch the script by following command :
```bash
$ python3 ADEM_Onboarding.py
```
if succesfull your script should end with the message "script ended succefully"<br>
if unsuccesfull your script should end with message "sceript ended with issues"
