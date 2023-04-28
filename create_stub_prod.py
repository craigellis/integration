import argparse
import requests
import json


# please get the correct PROD ClIENT_ID, CLIENT_SECRET and AUDIENCE from your local ORM Integration staff member.
CLIENT_ID =  "client_id - from Auth0"
CLIENT_SECRET = "clinet_secret from Auth0"
AUDIENCE = "audience URL from Auth0"
true = True 

parser = argparse.ArgumentParser(description='A simple CLI that creates an Auth0 stub')
parser.add_argument('name', help='The name of the connection to create')
args = parser.parse_args()


#Get Auth0 API token to create the connection
def get_token():

    payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "audience": AUDIENCE, "grant_type": "client_credentials"}
    conn = requests.post("https://learning.oreilly.auth0app.com/oauth/token", data=payload)
    j_conn = json.loads(conn.text)
    token = "Bearer " + j_conn['access_token']
    return token

#Actually create the stub connection in Auth0
def create_stub(token,name): 
	
	payload = {
   "name":name,
   "strategy":"samlp",
   "options":{
      "signingCert":"-----BEGIN CERTIFICATE-----MIICcDCCAdmgAwIBAgIBADANBgkqhkiG9w0BAQ0FADBUMQswCQYDVQQGEwJ1czETMBEGA1UECAwKQ2FsaWZvcm5pYTEZMBcGA1UECgwQSW50ZWdyYXRpb24gdGVhbTEVMBMGA1UEAwwMdGVzdC5mb28uYmFyMCAXDTIyMDcyOTIxMzQ1OVoYDzIwNTUwNjA2MjEzNDU5WjBUMQswCQYDVQQGEwJ1czETMBEGA1UECAwKQ2FsaWZvcm5pYTEZMBcGA1UECgwQSW50ZWdyYXRpb24gdGVhbTEVMBMGA1UEAwwMdGVzdC5mb28uYmFyMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDN+t6ikklCixc0QtPeurC/t6vOwxbjw4H1xkWkO+TFlj0ZOGo+L01e8ZgITeEFtNFf4+mAm2UCFkerQPt6CXLnbeUR36ePMnD58a/vIdjZD5XHmU4gtGKA4FzAtkxdFtuc/JT9DX8vXjnYiIA/BzgiSm7tmEZgRhuocC5dd/K4MQIDAQABo1AwTjAdBgNVHQ4EFgQUXF0zxV+JwR1H9Pm1tkVPxS7TexYwHwYDVR0jBBgwFoAUXF0zxV+JwR1H9Pm1tkVPxS7TexYwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQ0FAAOBgQAYExSWrc/NmBw0j29yZ3ltTv8w0l9Tv8DieCicEmemxs6pENAXQFhOvwsFFg1Hk//6JljLrovHMUVqzaRpfIdqJO3PfvNcacQtvaExZLDCI6+IeaT1ikFkZDJG8q9ISrT5c7ORy+f2l8WeRDEILdqPQNfRAVP8N0mznmbg/SiPVw==-----END CERTIFICATE-----",
      "signInEndpoint":"http://www.foo.bar",
      "debug":True,
      "digestAlgorithm":"sha256",
      "signSAMLRequest":"true",
      "signatureAlgorithm":"rsa-sha256",
      "idpinitiated":{
         "enabled":True,
         "client_id":"aq4IqDbVPDqgLtvsoUrPe08ooCNvO28e",
         "client_authorizequery":"response_type=code&scope=openid profile email"
      }
   }
}



	jpayload = json.dumps(payload)
	headers = {'Content-Type':'Application/json', 'Authorization': token}

	conn = requests.post("https://learning.oreilly.auth0app.com/api/v2/connections", data=jpayload, headers=headers)
	stuff = conn.json()
	
	returned_id = stuff["id"]
	returned_name = stuff["name"] 

	return returned_id, returned_name

#Create the GO link
def create_yourl(name):

	yourls_token = "yourls_token". # talk to integration staff member for correct yourls token
	auth0_long_url = f"https://sso.oreilly.com/authorize?client_id=tjyknUueLDUJgHQkwL3eEF4XeEhK9veC&protocol=oauth2&response_type=code&scope=openid%20profile%20email&redirect_uri=https://api.oreilly.com/api/v1/auth/oauth/complete/enterprise/&connection={name}"
	yourls_api_url = f"https://go.oreilly.com/yourls-api.php?signature={yourls_token}&action=shorturl&keyword={name}&format=json&url={auth0_long_url}"

	response = requests.get(yourls_api_url)
	jresponse = response.json()
	status = jresponse["status"]

	return status

name = args.name
token = get_token()

auth0_id, auth0_name  = create_stub(token,name)
yourls_status = create_yourl(name)

print("Auth0 id:",auth0_id)
print("Name: ",auth0_name)

print("Yourls creation status:", yourls_status)

print("end of script")	

