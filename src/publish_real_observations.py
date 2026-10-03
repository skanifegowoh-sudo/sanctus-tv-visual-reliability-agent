import os
import json,time,uuid
from aws_event_sink import AwsEventSink
API=os.environ.get('SANCTUS_HEALTH_API','')
d=json.load(open('evidence/milestone10-diverse-campaign.json'));sink=AwsEventSink(API);out=[]
for c in d['channels']:
 assessment=c['assessment']; condition='healthy' if assessment=='HEALTHY_SAMPLE' else ('inconclusive' if assessment=='INCONCLUSIVE' else 'attention')
 ev={'channel_id':c['channel_id'],'trace_id':'real-'+str(uuid.uuid4()),'timestamp':time.time(),'perception':{'source':'opencv5_real_stream_passive','condition':condition,'frames_read':c['frames_read'],'samples':c['samples'],'conditions':c['conditions'],'group':c['group'],'name':c['name']},'decision':{'state':'OBSERVATION_ONLY','assessment':assessment},'action':'OBSERVE_ONLY','human_approval_required':False,'outcome':assessment}
 try:r=sink.send(ev);out.append({'channel_id':c['channel_id'],'status':r['status'],'trace_id':ev['trace_id']})
 except Exception as e:out.append({'channel_id':c['channel_id'],'status':'ERROR','error':str(e)})
 time.sleep(.05)
open('evidence/milestone11-aws-publish.json','w').write(json.dumps(out,indent=2)+'\n')
print('stored',sum(x['status']==201 for x in out),'of',len(out));print(json.dumps(out,indent=2))
