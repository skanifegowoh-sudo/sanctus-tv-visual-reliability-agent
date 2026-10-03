import cv2,json,sys
from health_engine_v2 import TemporalVisualHealthEngine
def run(path):
 cap=cv2.VideoCapture(path);fps=cap.get(cv2.CAP_PROP_FPS) or 25;e=TemporalVisualHealthEngine();out=[];i=0
 while True:
  ok,f=cap.read()
  if not ok:break
  out.append(e.analyze(f,i/fps));i+=1
 cap.release();return out
expected={'healthy':'healthy','freeze':'frozen','black':'black_or_blank','low_motion':'healthy'}
rows=[]
for n,w in expected.items():
 d=run('tests/'+n+'.mp4');got=d[-1]['condition'];rows.append({'case':n,'expected':w,'final':got,'correct':got==w,'first_detection_s':next((x['timestamp'] for x in d if x['condition']==w and w!='healthy'),None)})
print(json.dumps(rows,indent=2))
assert all(x['correct'] for x in rows)
