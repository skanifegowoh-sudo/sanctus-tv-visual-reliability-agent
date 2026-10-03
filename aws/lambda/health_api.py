import json,os,time,decimal
TABLE=os.environ.get('HEALTH_TABLE','SanctusStreamHealth')
def _ddb():
 import boto3;return boto3.resource('dynamodb').Table(TABLE)
def response(code,body):return {'statusCode':code,'headers':{'content-type':'application/json','access-control-allow-origin':'*'},'body':json.dumps(body,default=str)}
def handler(event,context):
 method=(event.get('requestContext',{}).get('http',{}).get('method') or event.get('httpMethod','GET')).upper(); path=event.get('rawPath') or event.get('path','/')
 if method=='POST' and path.endswith('/health-events'):
  try:data=json.loads(event.get('body') or '{}')
  except:return response(400,{'error':'invalid_json'})
  required=['channel_id','trace_id','perception','decision','action']
  if any(k not in data for k in required):return response(400,{'error':'missing_required_fields','required':required})
  item={'channel_id':str(data['channel_id']),'event_ts':str(data.get('timestamp',time.time()))+'#'+str(data['trace_id']),'trace_id':str(data['trace_id']),'perception':data['perception'],'decision':data['decision'],'action':str(data['action']),'human_approval_required':bool(data.get('human_approval_required',False)),'outcome':data.get('outcome','PENDING')}
  _ddb().put_item(Item=json.loads(json.dumps(item),parse_float=decimal.Decimal));return response(201,{'stored':True,'channel_id':item['channel_id'],'trace_id':item['trace_id']})
 if method=='GET' and '/channels/' in path and path.endswith('/history'):
  channel=path.split('/channels/',1)[1].rsplit('/history',1)[0]
  from boto3.dynamodb.conditions import Key
  r=_ddb().query(KeyConditionExpression=Key('channel_id').eq(channel),ScanIndexForward=False,Limit=50);return response(200,{'channel_id':channel,'events':r.get('Items',[])})
 if method=='GET' and path.endswith('/healthz'):return response(200,{'service':'sanctus-stream-health','status':'ok'})
 return response(404,{'error':'not_found'})
