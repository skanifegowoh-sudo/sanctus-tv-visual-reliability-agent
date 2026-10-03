from dataclasses import dataclass,asdict
@dataclass
class HealthState:
 channel_id:str; state:str='HEALTHY'; suspicion_count:int=0; retry_count:int=0; max_retries:int=2; last_action:str='NONE'
 def apply(self,probe):
  prev=self.state; visual=probe.get('conditions',{}); ps=probe.get('probe_state'); bad=ps=='NO_FRAMES' or visual.get('black_or_blank',0) or visual.get('frozen',0)
  if bad:
   if self.state=='HUMAN_REVIEW': self.last_action='AWAIT_HUMAN_DECISION'; return {'previous_state':prev,**asdict(self)}
   self.suspicion_count+=1
   if self.suspicion_count<2:self.state='SUSPECTED_DEGRADATION';self.last_action='COLLECT_MORE_EVIDENCE'
   elif self.retry_count<self.max_retries:self.state='CONFIRMED_FAILURE';self.retry_count+=1;self.last_action='SAFE_RETEST'
   else:self.state='HUMAN_REVIEW';self.last_action='REQUEST_HUMAN_APPROVAL'
  else:
   self.suspicion_count=0;self.retry_count=0;self.state='HEALTHY';self.last_action='NONE'
  return {'previous_state':prev,**asdict(self)}
