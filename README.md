# PrismaAccess-ADEM-AutoOnboarding
When onboarding ADEM you have to create all the FQDN Objects and Policy as described in [this palo alto networks doc](https://docs.paloaltonetworks.com/autonomous-dem/autonomous-dem-admin/get-started-with-adem/enable-adem-for-mobile-users/enable-adem-in-cloud-managed-pa-mu#enable-autonomous-dem-in-cloud-managed-prisma-access)

# Prerequisites

Define a Prisma Access Tenant `Service Account`, here is a [howto](https://docs.paloaltonetworks.com/common-services/identity-and-access-access-management/manage-identity-and-access/add-service-accounts)

This service account is required in order to create an access token to use the API infrastructure of your Prisma Acces Tenant

Make sure that you have python's `requests` module installed
```bash
$ pip3 install requests
```

# What it can do

- This only works for Prisma Access Cloud Management
- Auto Generate all required ADEM FQDN objects under Shared Level
- Auto Generate a Dynamic Address group that consists all the ADEM FQDN objects
- Auto Generate a Pre-Rule Policy to allow traffic towards the ADEM FQND Service Objects

# what it cannot do

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
This script is leveraging the Prisma Access Cloud Mgmt API infrastructure.
In order to leverage the API calls we need to create a Bearer Token to perform the calls.
- Prisma Access Tenant Service Account [documentation](https://pan.dev/sase/docs/getstarted/)
- Bearer token [documentation](https://pan.dev/sase/docs/access-tokens/)


If there is no bearer token yet the script will prompt you to authenticate using the Tenant Service Acccount 

The Bearer Token is generated via the Oauth2 protocol using the palo alto networks Prisma Access `Tenant Service Account` these will be saved in the local directory under auth.txt. Once we have the auth information we can generate a Bearer token from the service account info. 

Bearer Tokens are only valid for 15min. 
This is the reason why there is a TokenVerify function, this will verify if the authentication informaton is present or expired.
- In case it is expired we will delete the auth.txt file and it will restart the authentication proces.
- In case the auth.txt file is not present , this indicates that you have not authenticated yet and the authenticaton proces will be initiated.
- In case the auth.txt file is present and not expired, the script will auto generate the bearor tokeen without reinitiating the authenticatioin proces

Once authenticaton and Token generation has been succesfull,
the script will start using the bearor token to push the FQDN objects, Dynamic Address Group and PreRule all in Shared Level. 


# How to use
when the github respoistory has been downloaded launch the script by following command :
```bash
$ python3 ADEM_Onboarding.py
```
Follow the terminal instructions that will be prompted. 
if succesfull your script should end with the message "script ended succefully"
if unsuccesfull your script should end with message "sceript ended with issues"
