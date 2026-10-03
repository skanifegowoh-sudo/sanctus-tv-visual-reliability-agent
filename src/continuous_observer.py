import json,subprocess,time,uuid,sys,os
from aws_event_sink import AwsEventSink
API=os.environ.get("SANCTUS_HEALTH_API","")
targets=sys.argv[1] if len(sys.argv)>1 else "/tmp/m10-campaign.tsv"
rounds=int(sys.argv[2]) if len(sys.argv)>2 else 2
sink=AwsEventSink(API); runs=[]
for n in range(rounds):
    started=time.time()
    outdir=f"evidence/observer-round-{n+1}"
    subprocess.run([".venv/bin/python","src/campaign_runner.py",targets,outdir],check=True,timeout=120,capture_output=True,text=True)
    report=json.load(open(outdir+"/campaign-report.json")); stored=0
    for c in report["channels"]:
        ev={"channel_id":c["channel_id"],"trace_id":"observer-"+str(uuid.uuid4()),"timestamp":time.time(),
            "perception":{"source":"opencv5_continuous_observer","condition":"healthy" if c["assessment"]=="HEALTHY_SAMPLE" else c["assessment"].lower(),"name":c["name"],"group":c["group"],"frames_read":c["frames_read"],"samples":c["samples"],"conditions":c["conditions"]},
            "decision":{"state":"OBSERVATION_ONLY","assessment":c["assessment"]},"action":"OBSERVE_ONLY","human_approval_required":False,"outcome":c["assessment"]}
        try: stored += sink.send(ev)["status"]==201
        except Exception: pass
    runs.append({"round":n+1,"elapsed_s":round(time.time()-started,2),"summary":report["summary"],"aws_201":stored,"events":len(report["channels"])})
    if n+1<rounds: time.sleep(2)
result={"mode":"CONTINUOUS_OBSERVER_VALIDATION","rounds":runs,"production_actions":0,"note":"Competition validation cadence only; destructive and source-changing actions remain disabled."}
open("evidence/milestone12-observer.json","w").write(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
