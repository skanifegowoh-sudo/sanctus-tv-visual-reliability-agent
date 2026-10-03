import csv,json,subprocess,concurrent.futures,time,os,sys
targets=sys.argv[1] if len(sys.argv)>1 else '/tmp/m10-campaign.tsv'
outdir=sys.argv[2] if len(sys.argv)>2 else 'evidence/real-campaign-concurrent'
os.makedirs(outdir,exist_ok=True)
rows=[]
with open(targets) as f:
 for r in csv.reader(f,delimiter='\t'):
  if len(r)>=4: rows.append({'channel_id':r[0],'name':r[1],'group':r[2],'url':r[3]})
def probe(x):
 started=time.time();p=os.path.join(outdir,x['channel_id']+'.json')
 try:
  cp=subprocess.run(['.venv/bin/python','src/live_probe_v2.py',x['url'],x['channel_id'],'10'],capture_output=True,text=True,timeout=18)
  if cp.returncode==0 and cp.stdout.strip():
   d=json.loads(cp.stdout);open(p,'w').write(json.dumps(d,indent=2)+'\n')
   cond=d.get('conditions',{});state='ATTENTION' if cond.get('frozen') or cond.get('black_or_blank') else ('INCONCLUSIVE' if d.get('frames_read',0)==0 else 'HEALTHY_SAMPLE')
  else:d={};state='INCONCLUSIVE'
 except Exception as e:d={};state='INCONCLUSIVE'
 return {'channel_id':x['channel_id'],'name':x['name'],'group':x['group'],'assessment':state,'frames_read':d.get('frames_read',0),'samples':d.get('samples',0),'conditions':d.get('conditions',{}),'elapsed_s':round(time.time()-started,2)}
started=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(probe,rows))
report={'mode':'PASSIVE_BOUNDED_CONCURRENT','max_workers':3,'per_channel_deadline_s':18,'production_actions':0,'elapsed_s':round(time.time()-started,2),'channels':results,'summary':{k:sum(r['assessment']==k for r in results) for k in ['HEALTHY_SAMPLE','ATTENTION','INCONCLUSIVE']}}
open(outdir+'/campaign-report.json','w').write(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
