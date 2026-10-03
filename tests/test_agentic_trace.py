import sys,json;sys.path.insert(0,'src');from orchestrator import HealthOrchestrator
o=HealthOrchestrator('demo-channel')
a=o.ingest({'probe_state':'NO_FRAMES','conditions':{}});assert a['action']=='COLLECT_MORE_EVIDENCE' and not a['human_approval_required']
b=o.ingest({'probe_state':'NO_FRAMES','conditions':{}});assert b['action']=='SAFE_RETEST' and b['human_approval_required']
c=o.verify({'probe_state':'VISUAL_EVIDENCE_AVAILABLE','conditions':{'healthy':20}});assert c['outcome']=='RECOVERED' and c['decision']['state']=='HEALTHY'
o.save('evidence/agentic-recovery-trace.json');print('agentic trace PASS:',a['action'],'->',b['action'],'->',c['outcome'])
