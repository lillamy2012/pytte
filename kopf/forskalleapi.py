import requests
import json


passw='zBLOf2@7'
user='Elin.Axelsson'

s = requests.Session()
auth = { 'username': user , 'password': passw }
r = s.post('http://ngs.csf.ac.at/forskalle/api/login', data=auth)
if (r.status_code != 200):
    raise Exception('Authentication error?')
    
r = s.get('http://ngs.csf.ac.at/forskalle/api/samples?group=Berger&since=99+years')
        # XXX of course you should always check the status code!
allsamples = r.json()

with open("group.json", "w") as outfile:
    json.dump(allsamples, outfile)

#s = s.get('http://ngs.csf.ac.at/forskalle/api/requests?group=Berger')

#allsamples = s.json()

#with open("groupReq.json", "w") as outfile:
#   json.dump(allsamples, outfile)