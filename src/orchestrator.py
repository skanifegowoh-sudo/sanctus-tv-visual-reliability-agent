import json,time,uuid
from state_machine import HealthState
class HealthOrchestrator:
 def __init__(self,channel_id): self.health=HealthState(channel_id); self.trace=[]
 def ingest(self,probe):
  decision=self.health.apply(probe); action=decision['last_action']; ev={'trace_id':str(uuid.uuid4()),'timestamp':time.time(),'channel_id':self.health.channel_id,'perception':probe,'decision':decision,'action':action,'human_approval_required':decision['state']=='CONFIRMED_FAILURE'};self.trace.append(ev);return ev
 def verify(self,probe):
  before=self.health.state; ev=self.ingest(probe); ev['verification_of']=before; ev['outcome']='RECOVERED' if before!='HEALTHY' and ev['decision']['state']=='HEALTHY' else ('STILL_UNHEALTHY' if ev['decision']['state']!='HEALTHY' else 'HEALTHY');return ev
 def save(self,path):open(path,'w').write(json.dumps(self.trace,indent=2)+'\n')
