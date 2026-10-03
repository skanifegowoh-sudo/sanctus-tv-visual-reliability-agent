import sys,json,types
sys.path.insert(0,'aws/lambda')
class Table:
 def __init__(self):self.items=[]
 def put_item(self,Item):self.items.append(Item);return {}
 def query(self,**kw):return {'Items':list(reversed(self.items))[:50]}
t=Table(); fake=types.SimpleNamespace(resource=lambda name:types.SimpleNamespace(Table=lambda name:t));sys.modules['boto3']=fake
# provide conditions module used by GET
m=types.ModuleType('boto3.dynamodb.conditions')
class K:
 def __init__(self,k):self.k=k
 def eq(self,v):return ('eq',self.k,v)
m.Key=K;sys.modules['boto3.dynamodb']=types.ModuleType('boto3.dynamodb');sys.modules['boto3.dynamodb.conditions']=m
import health_api
h=health_api.handler({'rawPath':'/healthz','requestContext':{'http':{'method':'GET'}}},None);assert h['statusCode']==200
e={'channel_id':'demo','trace_id':'abc','timestamp':1.2,'perception':{'condition':'frozen'},'decision':{'state':'CONFIRMED_FAILURE'},'action':'SAFE_RETEST'}
r=health_api.handler({'rawPath':'/health-events','requestContext':{'http':{'method':'POST'}},'body':json.dumps(e)},None);assert r['statusCode']==201 and len(t.items)==1
r=health_api.handler({'rawPath':'/channels/demo/history','requestContext':{'http':{'method':'GET'}}},None);assert r['statusCode']==200 and 'abc' in r['body']
print('AWS Lambda API contract PASS: healthz + store event + history')
