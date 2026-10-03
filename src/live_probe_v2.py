import cv2,time,json,sys
from health_engine_v2 import TemporalVisualHealthEngine
url,channel=sys.argv[1],sys.argv[2];seconds=float(sys.argv[3]) if len(sys.argv)>3 else 20
cap=cv2.VideoCapture(url,cv2.CAP_FFMPEG);eng=TemporalVisualHealthEngine();start=time.time();out=[];reads=0
while time.time()-start<seconds:
 ok,frame=cap.read()
 if not ok:time.sleep(.15);continue
 reads+=1
 if reads%10==0:out.append(eng.analyze(frame,time.time()))
cap.release();conditions={}
for e in out:conditions[e['condition']]=conditions.get(e['condition'],0)+1
print(json.dumps({'channel_id':channel,'probe_duration_s':round(time.time()-start,2),'frames_read':reads,'samples':len(out),'probe_state':'NO_FRAMES' if reads==0 else 'VISUAL_EVIDENCE_AVAILABLE','conditions':conditions,'evidence':out}))
