import cv2,numpy as np,os
OUT='tests';fps=10;size=(320,180);four=cv2.VideoWriter_fourcc(*'mp4v')
def moving(i):
 f=np.full((180,320,3),75,np.uint8);cv2.rectangle(f,(20+(i*4)%250,65),(70+(i*4)%250,115),(220,220,220),-1);cv2.putText(f,f'LIVE {i:03d}',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.55,(255,255,255),1);return f
def write(n,fs):
 w=cv2.VideoWriter(os.path.join(OUT,n),four,fps,size)
 for f in fs:w.write(f)
 w.release()
healthy=[moving(i) for i in range(140)]; frozen=moving(19)
write('stall_then_recover.mp4',healthy[:20]+[frozen.copy() for _ in range(65)]+healthy[85:140])
write('black_then_recover.mp4',healthy[:20]+[np.zeros((180,320,3),np.uint8) for _ in range(45)]+healthy[65:140])
write('stall_never_recovers.mp4',healthy[:20]+[frozen.copy() for _ in range(120)])
print('generated recovery cases')
