import json,urllib.request
class AwsEventSink:
 def __init__(self,base_url,api_key=None):self.url=base_url.rstrip('/');self.api_key=api_key
 def send(self,event,timeout=8):
  body=json.dumps(event).encode();headers={'content-type':'application/json'}
  if self.api_key:headers['x-api-key']=self.api_key
  req=urllib.request.Request(self.url+'/health-events',data=body,headers=headers,method='POST')
  with urllib.request.urlopen(req,timeout=timeout) as r:return {'status':r.status,'body':json.loads(r.read())}
