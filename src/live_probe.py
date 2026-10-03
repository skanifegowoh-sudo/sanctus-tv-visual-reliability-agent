import cv2,time,json,sys
from health_engine import VisualHealthEngine
url=sys.argv[1]; channel=sys.argv[2]; seconds=float(sys.argv[3]) if len(sys.argv)>3 else 12
cap=cv2.VideoCapture(url,cv2.CAP_FFMPEG); eng=VisualHealthEngine(); start=time.time(); out=[]; reads=0
while time.time()-start<seconds:
 ok,frame=cap.read()
 if not ok:
  time.sleep(.15);continue
 reads+=1
 if reads%10==0:out.append(eng.analyze(frame,time.time()))
cap.release()
summary={'channel_id':channel,'probe_duration_s':round(time.time()-start,2),'frames_read':reads,'samples':len(out),'probe_state':('NO_FRAMES' if reads==0 else 'VISUAL_EVIDENCE_AVAILABLE'),'conditions':{},'evidence':out}
for e in out:summary['conditions'][e['condition']]=summary['conditions'].get(e['condition'],0)+1
print(json.dumps(summary))
