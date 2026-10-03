from pathlib import Path
import json, hashlib, re
ROOT=Path('/state/paseo/worktrees/3detpo3k/feat-bedrock2-executable-verbs')
OUT=Path('/tmp/bedrock2-executable-draft')
OUT.mkdir(exist_ok=True)
GRAPH='ac91c8dda973281bcc2b732886bdac8abf6ee30b'
CLIENT='f4dad5ba6c989e5aaf0896b7dd1ccd8e49fd3c37'
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2)+'\n')
def expr(step,field='made'): return '${'+step+'.'+field+'}'
steps=[]
def act(key,verb,payload,role,check=None):
    args={'op':'act','verb':verb,'level':'repository','scope':'${scope}','payload':payload,'request_id':'${run}:'+key}
    steps.append({'key':key,'role':role,'arguments':args,'check':check or {}})
def query(key,name,params,check=None):
    steps.append({'key':key,'role':'scout','arguments':{'op':'query','name':name,'params':params},'check':check or {}})
def pointer(key,title,path):
    steps.append({'key':key,'role':'scout','arguments':{'op':'reference.put','level':'repository','scope':'${scope}','reference':{'title':title,'kind':'repository_file','repository':'cleverunicornz/yeetz-bedrock-protocol','commit':'${fixture_commit}','path':path},'request_id':'${run}:'+key},'check':{'state':'stored'}})
pointer('instruction','Accepted fixture specification','contract/tool-examples/probe.py')
pointer('evidence','Fixture probe source','contract/tool-examples/probe.py')
act('stipulate','stipulate',{'invariant':{'title':'Fixture observations keep their source','rule':'Every fixture observation points to its evidence.','priority':'standard'}},'authority',{'state':'stipulated'})
act('declare','declare',{'gap':{'title':'Fixture coverage is unobserved','statement':'The isolated replay has not yet observed an empty-list parse.'}},'implementer',{'state':'declared'})
act('formulate','formulate',{'responds_to':[expr('declare')],'candidate':{'title':'Run the empty-list probe','hypothesis':'Parsing the fixture empty JSON list produces an empty list.'}},'scout',{'state':'formulated'})
act('evaluate','evaluate',{'candidate':expr('formulate'),'outcome':'favourable','findings':[expr('evidence')],'note':'The fixture probe supplies a concrete result.'},'scout',{'subject':expr('formulate'),'state':'evaluated','outcome':'favourable'})
act('decide','decide',{'considered':[expr('declare'),expr('formulate')],'outcomes':[{'subject':expr('formulate'),'outcome':'accept'},{'subject':expr('declare'),'outcome':'keep'}],'decision':{'title':'Accept the empty-list fixture','statement':'Accept the Candidate within the isolated replay.','why':'The fixture source defines a deterministic observation.'}},'authority',{'state':'decided'})
act('mint','mint',{'basis':{'decision':expr('decide')},'from_candidate':expr('formulate'),'addresses':[expr('declare')],'promise':{'title':'The fixture empty list parses','statement':'Parsing [] produces an empty list.','scope':'The isolated fixture probe.'}},'orchestrator',{'state':'asserted'})
act('define','define',{'oracle':{'title':'Check the empty-list probe','judges':expr('mint'),'inputs':'The fixture probe result and pinned source.','holds_when':'The result is an empty list.','fails_when':'The result differs from an empty list.','arrangement':'deterministic'}},'orchestrator',{'state':'defined'})
act('produce','produce',{'witness':{'title':'Empty-list fixture observation','observes':expr('mint'),'observed_at':'${observed_at}','coordinate':'${fixture_commit}','result':'${probe_result}','evidence':[expr('evidence')]}},'implementer',{'state':'produced'})
act('judge','judge',{'promise':expr('mint'),'oracle':expr('define'),'witness':expr('produce'),'verdict':'holds','reason':'The fixture result is an empty list.'},'validator',{'subject':expr('mint'),'state':'assured'})
query('assure','assured_by',{'promise':expr('mint')},{'state':'assured','standing_act':expr('judge','act_id')})
act('refine','refine',{'target':expr('declare'),'sighting':{'note':'The independent fixture replay sees the same coverage need.','evidence':[expr('evidence')]}},'scout',{'subject':expr('declare'),'state':'decided'})
act('refine_candidate','refine',{'target':expr('formulate'),'sighting':{'note':'The same probe is usable by another reader.','evidence':[expr('evidence')]}},'scout',{'subject':expr('formulate'),'state':'decided'})
act('refine_witness','refine',{'target':expr('produce'),'witness':{'title':'Repeated empty-list fixture observation','observes':expr('mint'),'observed_at':'${observed_at}','coordinate':'${fixture_commit}','result':'${probe_result}','evidence':[expr('evidence')]}},'implementer',{'state':'produced'})
act('judge_inconclusive','judge',{'promise':expr('mint'),'oracle':expr('define'),'witness':expr('refine_witness'),'verdict':'inconclusive','reason':'This fixture verdict demonstrates an inconclusive round.'},'validator',{'subject':expr('mint'),'state':'assured'})
act('judgment_gap','declare',{'arose_in':expr('judge','act_id'),'about':[expr('mint')],'gap':{'title':'Fixture deployment is unqualified','statement':'The isolated receiver uses test identity; deployment trust was not exercised.'}},'validator',{'state':'declared'})
act('successor','declare',{'gap':{'title':'Fixture runtime qualification is absent','statement':'Runtime registration and deployed tool invocation remain outside this isolated replay.'}},'scout',{'state':'declared'})
act('supersede','supersede',{'target':expr('judgment_gap'),'successor':expr('successor'),'reason':'The successor states the observed limit more precisely.'},'authority',{'subject':expr('judgment_gap'),'state':'superseded'})
act('revoke','revoke',{'target':expr('produce'),'reason':'Withdraw the fixture observation to exercise assurance recomputation.'},'implementer',{'subject':expr('mint'),'state':'asserted'})
act('witness_successor','produce',{'witness':{'title':'Independent current fixture Witness','observes':expr('mint'),'observed_at':'${observed_at}','coordinate':'${fixture_commit}','result':'${probe_result}','evidence':[expr('evidence')]}},'implementer',{'state':'produced'})
query('assure_after_revoke','assured_by',{'promise':expr('mint')},{'state':'asserted','standing_act':None})
query('binds','binds',{'level':'repository','scope':'${scope}'})
query('open_work','open_work',{'level':'repository','scope':'${scope}'})
steps.append({'key':'reference_get','role':'scout','arguments':{'op':'reference.get','id':expr('evidence')},'check':{'state':'stored'}})
# Public calls never include receiver identity or allocated IDs. Role is solely
# fixture configuration and is not projected into either request envelope.
negatives=[
{'key':'duplicate_judge','role':'validator','arguments':{'op':'act','verb':'judge','level':'repository','scope':'${scope}','payload':{'promise':expr('mint'),'oracle':expr('define'),'witness':expr('refine_witness'),'verdict':'holds','reason':'Duplicate pair fixture.'},'request_id':'${run}:duplicate_judge'},'refusal':'already_judged'},
{'key':'missing_input','role':'scout','arguments':{'op':'act','verb':'formulate','level':'repository','scope':'${scope}','payload':{'responds_to':['G-fixture-absent'],'candidate':{'title':'Invalid fixture','hypothesis':'No recorded basis exists.'}},'request_id':'${run}:missing_input'},'refusal':'missing_input'},
{'key':'supersede_witness','role':'authority','arguments':{'op':'act','verb':'supersede','level':'repository','scope':'${scope}','payload':{'target':expr('refine_witness'),'successor':expr('witness_successor'),'reason':'Invalid fixture.'},'request_id':'${run}:supersede_witness'},'refusal':'transition_not_allowed'}]
dump(OUT/'contract/tool-examples/calls.json',{'format':1,'steps':steps,'negative_steps':negatives,'note':'Role labels configure the isolated test receiver only; no role is a caller argument. This is a protocol fixture, not deployed authority.'})
primary={s['key']:s for s in steps}
for verb in ['stipulate','declare','formulate','evaluate','decide','mint','define','produce','refine','judge','assure','revoke','supersede']:
    args=primary[verb]['arguments']
    if args['op']=='act':
        native={k:args[k] for k in ('verb','level','scope','payload','request_id')}
        native['session']='${session}'
        method='POST /v1/acts'
        subject=primary[verb]['check'].get('subject',expr(verb))
        read={'op':'query','name':'record','params':{'id':subject}}
        prerequisites=sorted(set(re.findall(r'\$\{([^}]+)\}',json.dumps(args)))-{'run','scope','observed_at','fixture_commit','probe_result'})
        prep='Resolve '+', '.join('`'+p+'`' for p in prerequisites)+' from successful preceding responses. ' if prerequisites else ''
        after='Retain `act_id`, `made`, `seq`, `recorded_at`, `changes` and any edit-window fields. '+('This act makes no record; `made` is null. ' if verb in ('evaluate','judge','revoke','supersede','refine') else 'Bind the returned `made` before any dependent call. ')
    else:
        native={k:args[k] for k in ('name','params')}
        method='POST /v1/query'
        read={'op':'query','name':'record','params':{'id':expr('mint')}}
        prep='Resolve `mint.made` from the successful mint response. '
        after='Read `state`, `standing` and `since`. An assured Promise has `state` equal to `assured` and a standing holds judgment. No assure act is submitted. '
    procedure='''\n\n## Executable procedure\n\nUse the pinned receiver interface in `contract/tool-interface.md` and\n`contract/tool-interface.json`. The JSON below is the exact client argument\nshape after substitution. `${scope}` is the admitted scope; `${run}` is a\nunique replay prefix. `${step.field}` binds a field from an earlier successful\nresponse in `contract/tool-examples/calls.json`; these substitutions are\nperformed before sending, never by the receiver. Never guess allocated IDs.\n\n'''+prep+'''The receiver stamps the actor and role; callers never supply\nactor, role, principal, allocated IDs or recording time. Preserve the verb's\nroles and meaning in the Contract table above.\n\n```json\n'''+json.dumps(args,indent=2)+'''\n```\n\nThe native request is `'''+method+'''`. `${session}` is discovered caller\nlineage added by the client, not a client argument. Its required envelope is:\n\n```json\n'''+json.dumps(native,indent=2)+'''\n```\n\n'''+after+'''Read back using this exact query:\n\n```json\n'''+json.dumps(read,indent=2)+'''\n```\n\nQuery answers carry `watermark` and `head`; check that projection has passed\nthe returned act sequence before interpreting the state. A lagging or absent\nprojection is not a refusal. On an uncertain write outcome, retain and repeat\nthe identical arguments and original request key; never allocate a new key\nfor that intent. The pinned client suppresses native refusal messages and\nraises an error containing the refusal code. Readback and replay limits are\nlisted in `contract/tool-interface.md`.\n'''
    if verb=='refine':
        procedure+='\nFor a Witness, use the complete `refine_witness` invocation in\n`contract/tool-examples/calls.json`: it makes a new Witness of the same Promise\nand returns its `made` ID. For a Gap or Candidate the sighting invocation\nabove makes no record; `made` is null. Neither form rewrites the observation.\n'
        procedure=procedure.replace('This act makes no record; `made` is null. ','The sighting form makes no record; `made` is null. ')
    if verb=='judge':
        procedure+='\nA `does_not_hold` invocation must include concrete `failure_evidence`\nReference IDs; `inconclusive` leaves the Promise state unchanged. Declare any\nfinding separately with `arose_in` bound to this response\'s `act_id`, as\n`judgment_gap` demonstrates in `contract/tool-examples/calls.json`.\n'
    if verb=='produce':
        procedure+='\n`${observed_at}`, `${fixture_commit}` and `${probe_result}` are actual probe\nvalues supplied by the isolated replay. For real work use its actual run\ntime, artifact coordinate, result and previously stored evidence References.\nA fixture observation is never a qualification of the deployed receiver.\n'
    source=(ROOT/f'contract/skills/{verb}/SKILL.md').read_text()
    target=OUT/f'contract/skills/{verb}/SKILL.md'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(source+procedure)
print('Prepared temporary complete skill draft; repository untouched.')
