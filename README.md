# PrismaAccess-ADEM-AutoOnboarding
When onboarding ADEM you have to create all the FQDN Objects and Policy as described in [this palo alto networks doc](https://docs.paloaltonetworks.com/autonomous-dem/autonomous-dem-admin/get-started-with-adem/enable-adem-for-mobile-users/enable-adem-in-cloud-managed-pa-mu#enable-autonomous-dem-in-cloud-managed-prisma-access)

# Prerequisites

Define a Prisma Access Tenant Service Account, [howto](https://docs.paloaltonetworks.com/common-services/identity-and-access-access-management/manage-identity-and-access/add-service-accounts)

This service account is required in order to create an access token to use the API infrastructure of your Prisma Acces Tenant

Make sure that you have python's `requests` module installed
```bash
$ pip3 install requests
```

# What it can do
# what it cannot do
# How It Works
This script is leveraging the Prisma Access Cloud Mgmt API infrastructure.
# how to use