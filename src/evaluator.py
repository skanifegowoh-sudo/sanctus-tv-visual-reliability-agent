import json,glob,os,time
EXPECTED={'healthy':'healthy','freeze':'frozen','black':'black_or_blank','low_motion':'healthy'}
rows=[]; correct=0; fp=0; negatives=0
for name,want in EXPECTED.items():
 d=json.load(open('evidence/'+name+'.json')); got=d[-1]['condition']; ok=got==want;correct+=ok
 if want=='healthy': negatives+=1;fp+=got!='healthy'
 first=next((x for x in d if x['condition']==want),None)
 rows.append({'case':name,'expected':want,'final':got,'correct':ok,'first_detection_s':None if not first else first['timestamp']})
report={'generated_at':time.time(),'opencv_cases':len(rows),'accuracy':correct/len(rows),'false_positive_rate_on_healthy_cases':fp/max(1,negatives),'cases':rows}
open('evidence/evaluation-summary.json','w').write(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
