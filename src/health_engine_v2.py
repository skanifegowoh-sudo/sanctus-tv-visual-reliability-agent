import cv2,numpy as np,time
from collections import deque
class TemporalVisualHealthEngine:
 def __init__(self,freeze_seconds=7.0,black_confirm_seconds=2.0,diff_threshold=.12,dark_level=18,black_ratio=.985):
  self.freeze_seconds=freeze_seconds;self.black_confirm_seconds=black_confirm_seconds;self.diff_threshold=diff_threshold;self.dark_level=dark_level;self.black_ratio=black_ratio
  self.prev=None;self.low_since=None;self.black_since=None;self.recent=deque(maxlen=12)
 def analyze(self,frame,ts=None):
  ts=time.time() if ts is None else ts;g=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  mean=float(g.mean());std=float(g.std());dark=float(np.mean(g<self.dark_level));raw_black=dark>=self.black_ratio and mean<self.dark_level
  if raw_black:
   if self.black_since is None:self.black_since=ts
  else:self.black_since=None
  black_dur=0 if self.black_since is None else max(0,ts-self.black_since);black=raw_black and black_dur>=self.black_confirm_seconds
  diff=None;changed=None
  if self.prev is not None:
   delta=cv2.absdiff(g,self.prev);diff=float(delta.mean());changed=float(np.mean(delta>3));score=max(diff,changed*10)
   self.recent.append(score)
   if score<self.diff_threshold:
    if self.low_since is None:self.low_since=ts
   else:self.low_since=None
  low_dur=0 if self.low_since is None else max(0,ts-self.low_since)
  # Confirmation requires sustained low change AND a recent window consistently below threshold.
  consistent=len(self.recent)>=4 and sum(x<self.diff_threshold for x in list(self.recent)[-4:])>=4
  frozen=(not raw_black) and low_dur>=self.freeze_seconds and consistent
  self.prev=g
  condition='black_or_blank' if black else ('frozen' if frozen else 'healthy')
  return {'timestamp':ts,'condition':condition,'mean_luma':round(mean,3),'luma_std':round(std,3),'dark_ratio':round(dark,5),'frame_diff':None if diff is None else round(max(diff,(changed or 0)*10),3),'freeze_duration_s':round(low_dur,2),'black_duration_s':round(black_dur,2),'temporal_confirmed':bool(black or frozen)}
