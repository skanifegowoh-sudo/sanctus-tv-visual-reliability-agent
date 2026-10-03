import cv2,json,sys,time
from health_engine import VisualHealthEngine
from orchestrator import HealthOrchestrator

def run(path,name):
 cap=cv2.VideoCapture(path);fps=cap.get(cv2.CAP_PROP_FPS) or 10;vision=VisualHealthEngine();agent=HealthOrchestrator(name);timeline=[];last_condition='healthy'; confirmed_at=None; recovered_at=None;i=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  ev=vision.analyze(frame,i/fps); condition=ev['condition']
  if condition!=last_condition:
   probe={'probe_state':'VISUAL_EVIDENCE_AVAILABLE','conditions':{condition:1},'visual_evidence':ev}; step=agent.ingest(probe);timeline.append({'t':round(i/fps,2),'condition':condition,'agent':step})
   if step['decision']['state']=='CONFIRMED_FAILURE' and confirmed_at is None:confirmed_at=i/fps
   if confirmed_at is not None and step['decision']['state']=='HEALTHY' and recovered_at is None:recovered_at=i/fps
   last_condition=condition
  elif condition in ('frozen','black_or_blank') and i%10==0:
   probe={'probe_state':'VISUAL_EVIDENCE_AVAILABLE','conditions':{condition:1},'visual_evidence':ev};step=agent.ingest(probe);timeline.append({'t':round(i/fps,2),'condition':condition,'agent':step})
   if step['decision']['state']=='CONFIRMED_FAILURE' and confirmed_at is None:confirmed_at=i/fps
  i+=1
 cap.release(); result={'case':name,'frames':i,'duration_s':round(i/fps,2),'confirmed_failure_at_s':confirmed_at,'recovered_at_s':recovered_at,'recovery_latency_s':None if confirmed_at is None or recovered_at is None else round(recovered_at-confirmed_at,2),'final_state':agent.health.state,'timeline':timeline};return result
if __name__=='__main__':
 r=run(sys.argv[1],sys.argv[2]);print(json.dumps(r,indent=2))
