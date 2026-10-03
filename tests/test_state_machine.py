import sys;sys.path.insert(0,'src');from state_machine import HealthState
s=HealthState('demo');assert s.apply({'probe_state':'VISUAL_EVIDENCE_AVAILABLE','conditions':{'healthy':5}})['state']=='HEALTHY'
a=s.apply({'probe_state':'NO_FRAMES','conditions':{}});assert a['state']=='SUSPECTED_DEGRADATION' and a['last_action']=='COLLECT_MORE_EVIDENCE'
a=s.apply({'probe_state':'NO_FRAMES','conditions':{}});assert a['state']=='CONFIRMED_FAILURE' and a['last_action']=='SAFE_RETEST'
a=s.apply({'probe_state':'VISUAL_EVIDENCE_AVAILABLE','conditions':{'healthy':5}});assert a['state']=='HEALTHY';print('state-machine PASS')
