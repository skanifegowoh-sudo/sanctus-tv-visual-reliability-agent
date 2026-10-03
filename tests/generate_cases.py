import cv2,numpy as np,os
OUT=os.path.dirname(__file__); four=cv2.VideoWriter_fourcc(*'mp4v'); fps=10; size=(320,180)
def write(name,frames):
 w=cv2.VideoWriter(os.path.join(OUT,name),four,fps,size)
 for f in frames:w.write(f)
 w.release()
# Healthy moving scene
frames=[]
for i in range(100):
 f=np.full((180,320,3),70,np.uint8); cv2.circle(f,(20+(i*3)%280,90),18,(220,220,220),-1); cv2.putText(f,str(i),(10,25),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),1);frames.append(f)
write('healthy.mp4',frames)
# True freeze after 2 sec
base=frames[19].copy(); write('freeze.mp4',frames[:20]+[base.copy() for _ in range(80)])
# Black after 2 sec
write('black.mp4',frames[:20]+[np.zeros((180,320,3),np.uint8) for _ in range(80)])
# Legitimate low-motion: mostly static but tiny clock changes each second
low=[]
for i in range(100):
 f=np.full((180,320,3),90,np.uint8); cv2.putText(f,'ADORATION',(70,85),cv2.FONT_HERSHEY_SIMPLEX,.8,(180,180,180),2);cv2.putText(f,f'{i:03d}',(145,120),cv2.FONT_HERSHEY_SIMPLEX,.5,(200,200,200),1);low.append(f)
write('low_motion.mp4',low)
