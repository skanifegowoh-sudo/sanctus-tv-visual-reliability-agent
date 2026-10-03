import cv2, numpy as np, json, time, argparse
from collections import deque

class VisualHealthEngine:
    def __init__(self, freeze_seconds=5.0, black_ratio=.985, dark_level=18, diff_threshold=.12):
        self.freeze_seconds=freeze_seconds; self.black_ratio=black_ratio; self.dark_level=dark_level; self.diff_threshold=diff_threshold
        self.prev=None; self.freeze_since=None; self.samples=deque(maxlen=30)
    def analyze(self, frame, ts=None):
        ts=time.time() if ts is None else ts
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        mean=float(gray.mean()); std=float(gray.std()); dark_ratio=float(np.mean(gray < self.dark_level))
        black=dark_ratio>=self.black_ratio and mean<self.dark_level
        diff=None; frozen=False; freeze_duration=0.0
        if self.prev is not None:
            delta=cv2.absdiff(gray,self.prev); diff=float(delta.mean()); changed_ratio=float(np.mean(delta>3)); diff=max(diff,changed_ratio*10.0)
            if diff < self.diff_threshold:
                if self.freeze_since is None:self.freeze_since=ts
                freeze_duration=max(0.0,ts-self.freeze_since); frozen=freeze_duration>=self.freeze_seconds
            else:self.freeze_since=None
        self.prev=gray
        condition='black_or_blank' if black else ('frozen' if frozen else 'healthy')
        evidence={'timestamp':ts,'condition':condition,'mean_luma':round(mean,3),'luma_std':round(std,3),'dark_ratio':round(dark_ratio,5),'frame_diff':None if diff is None else round(diff,3),'freeze_duration_s':round(freeze_duration,2)}
        self.samples.append(evidence); return evidence

def run_video(path, sample_every=1):
    cap=cv2.VideoCapture(path); eng=VisualHealthEngine(); out=[]; i=0; fps=cap.get(cv2.CAP_PROP_FPS) or 25
    while True:
        ok,frame=cap.read()
        if not ok:break
        if i%sample_every==0:out.append(eng.analyze(frame,i/fps))
        i+=1
    cap.release(); return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--json');a=ap.parse_args();r=run_video(a.video); s=json.dumps(r,indent=2)
    open(a.json,'w').write(s+'\n') if a.json else print(s)
