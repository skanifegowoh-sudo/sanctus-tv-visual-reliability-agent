import json,time
base=json.load(open('evidence/evaluation-summary.json'))
loops={}
for n in ['stall_then_recover','black_then_recover','stall_never_recovers']:
 d=json.load(open(f'evidence/{n}-loop.json'))
 loops[n]={k:d[k] for k in ['duration_s','confirmed_failure_at_s','recovered_at_s','recovery_latency_s','final_state']}
report={'milestone':9,'generated_at':time.time(),'scope':'controlled visual failure lab; not production accuracy','opencv_version':__import__('cv2').__version__,'classification':{'cases':base['opencv_cases'],'accuracy':base['accuracy'],'healthy_false_positive_rate':base['false_positive_rate_on_healthy_cases']},'closed_loop':loops,'claims_limit':'Metrics apply only to deterministic synthetic fixtures in this evaluation harness. Real-stream validation is a separate next phase.'}
open('evidence/milestone9-report.json','w').write(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
