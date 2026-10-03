import json,glob,os,time
rows=[]
for p in sorted(glob.glob('evidence/real-streams/*.json')):
 name=os.path.basename(p)[:-5]
 try:d=json.load(open(p))
 except Exception: rows.append({'channel_id':name,'probe_state':'PROBE_ERROR','frames_read':0,'conditions':{},'assessment':'INCONCLUSIVE'});continue
 cond=d.get('conditions',{}); frames=d.get('frames_read',0)
 if d.get('probe_state')!='VISUAL_EVIDENCE_AVAILABLE': assessment='INCONCLUSIVE'
 elif cond.get('frozen') or cond.get('black_or_blank'): assessment='ATTENTION'
 else: assessment='HEALTHY_SAMPLE'
 rows.append({'channel_id':name,'probe_state':d.get('probe_state'),'frames_read':frames,'samples':d.get('samples',0),'conditions':cond,'assessment':assessment})
report={'milestone':10,'generated_at':time.time(),'mode':'PASSIVE_OBSERVATION_ONLY','production_actions':0,'channels':rows,'summary':{'healthy_samples':sum(x['assessment']=='HEALTHY_SAMPLE' for x in rows),'attention':sum(x['assessment']=='ATTENTION' for x in rows),'inconclusive':sum(x['assessment']=='INCONCLUSIVE' for x in rows)},'interpretation':'Attention is visual evidence requiring a longer follow-up sample; it is not automatically a confirmed production outage.'}
open('evidence/milestone10-real-stream-pass1.json','w').write(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
