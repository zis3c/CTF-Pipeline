#!/usr/bin/env python3
"""Metadata, archive, index and safety layer for the CTFd pull pipeline."""
from __future__ import annotations
import hashlib, json, os, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(sys.argv[2]).resolve()
EVENT = ROOT.name
STATE = ROOT / '.pipeline'

def load_json(path):
    return json.loads(path.read_text()) if path.exists() else []

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'challenge'

def challenge_key(c): return (str(c.get('id','')), c.get('name',''))

def snapshot():
    STATE.mkdir(exist_ok=True)
    src = ROOT / 'challenges-detailed.json'
    if src.exists(): shutil.copy2(src, STATE / 'previous-challenges-detailed.json')

def diff(old, new):
    om={challenge_key(x):x for x in old}; nm={challenge_key(x):x for x in new}
    for k in sorted(nm.keys()-om.keys()): print('+ new:', nm[k].get('name'))
    for k in sorted(om.keys()-nm.keys()): print('- removed:', om[k].get('name'))
    fields=('name','category','type','value','description','connection_info','files','hints')
    for k in sorted(nm.keys() & om.keys()):
        changes=[f for f in fields if om[k].get(f)!=nm[k].get(f)]
        if changes: print('~ modified:', nm[k].get('name'), '['+', '.join(changes)+']')

def show_diff():
    old=load_json(STATE/'previous-challenges-detailed.json'); new=load_json(ROOT/'challenges-detailed.json')
    print('Resync diff:')
    diff(old,new)
    if old==new: print('  no metadata changes')

def dry_run():
    cfg=load_json(ROOT/'.ctfd/config.json') if (ROOT/'.ctfd/config.json').exists() else {}
    c=cfg.get('CTFD',{}); url=c.get('URL','').rstrip('/'); token=c.get('TOKEN','')
    if not url or not token: raise SystemExit('Profile is not initialized')
    response=requests.get(url+'/api/v1/challenges',headers={'Authorization':f'Token {token}','Content-Type':'application/json','User-Agent':'CTFd-CLI-v0.1-by-@TheFlash2k'},timeout=20)
    try: live=response.json().get('data',[])
    except ValueError: raise SystemExit(f'CTFd dry-run returned HTTP {response.status_code}, not JSON')
    old=load_json(ROOT/'challenges-detailed.json')
    print(f'Dry run for {EVENT}:')
    diff(old,live)
    if old==live: print('  no changes; nothing will be overwritten')

def archive():
    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ'); dest=ROOT/'.history'/stamp
    dest.mkdir(parents=True,exist_ok=True)
    for name in ('README.md','challenges.json','challenges-detailed.json'):
        p=ROOT/name
        if p.exists(): shutil.copy2(p,dest/name)
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in {'.ctfd','.pipeline','.history','.git','manual'}:
            shutil.copytree(p,dest/p.name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('work','notes','writeup','flag_output_dir','attachment-manifest.json','AGENT.md','EXECUTION-SAFETY.md'))
    print('Archived generated content:', dest)

def metadata():
    items=load_json(ROOT/'challenges-detailed.json'); now=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    cfg=load_json(ROOT/'.ctfd/config.json') if (ROOT/'.ctfd/config.json').exists() else {}
    c=cfg.get('CTFD',{})
    profile={'profile':EVENT,'ctfd_url':c.get('URL',''),'last_sync':now,'challenge_count':len(items),'token_status':'configured' if c.get('TOKEN') else 'missing'}
    p=ROOT/'.ctf-profile.json'; p.write_text(json.dumps(profile,indent=2)+'\n'); p.chmod(0o600)
    counts={}
    for x in items: counts[x.get('category','Other')]=counts.get(x.get('category','Other'),0)+1
    lines=[f'# {EVENT}', '', '## Profile', '', f"- CTFd URL: {c.get('URL','')}",f'- Last sync: {now}',f'- Challenges: {len(items)}', '', '## Categories', '', '| Category | Count |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in sorted(counts.items())]
    (ROOT/'_ctf-info.md').write_text('\n'.join(lines)+'\n')

def challenge_dir(item):
    cat=slug(item.get('category','other'))
    mapping={'cryptography':'crypto','web-exploitation':'web','binary-exploitation':'pwn','reverse-engineering':'reverse','digital-forensics':'forensics','mobile-exploitation':'mobile','miscellaneous':'misc','selamat-datang':'welcome','selamat-jalan':'welcome'}
    cat=mapping.get(cat,cat)
    return ROOT/cat/slug(item.get('name','challenge'))

def attachment_names(item):
    return {Path(str(f).split('?',1)[0]).name for f in (item.get('files') or [])}

def generated_docs():
    items=load_json(ROOT/'challenges-detailed.json'); index=['# Challenge Index','', '| Status | Category | Challenge | Points | ID |','|---|---|---|---:|---:|']
    for x in items:
        d=challenge_dir(x); d.mkdir(parents=True,exist_ok=True); (d/'work').mkdir(exist_ok=True); (d/'notes').mkdir(exist_ok=True); (d/'writeup').mkdir(exist_ok=True); (d/'flag_output_dir').mkdir(exist_ok=True); (d/'flag_output_dir').chmod(0o700)
        st=d/'.solver-status'
        if not st.exists(): st.write_text('not_started\n')
        status={'not_started':'[ ]','in_progress':'[~]','solved':'[x]'}.get(st.read_text().strip(),'[ ]')
        index.append(f"| {status} | {x.get('category','')} | [{x.get('name','')}]({d.relative_to(ROOT)}/) | {x.get('value','')} | {x.get('id','')} |")
        files=[]
        expected=attachment_names(x)
        for p in d.iterdir():
            if p.is_file() and p.name in expected:
                h=hashlib.sha256(p.read_bytes()).hexdigest(); files.append({'file':p.name,'size':p.stat().st_size,'sha256':h})
        (d/'attachment-manifest.json').write_text(json.dumps({'challenge':x.get('name'),'generated_at':datetime.now(timezone.utc).isoformat(),'files':files},indent=2)+'\n')
        family={'crypto':'ctf-crypto','pwn':'ctf-pwn','web':'ctf-web','forensics':'ctf-forensics','reverse':'ctf-reverse','osint':'ctf-osint','misc':'ctf-misc','mobile':'ctf-reverse','boot2root':'ctf-forensics'}.get(slug(x.get('category','')),'solve-challenge')
        repo_root = Path(os.environ.get('CTF_HOME', Path(__file__).resolve().parents[1])).resolve()
        agent=f"# Agent Context: {x.get('name','')}\n\n- Category: {x.get('category','')}\n- Type: {x.get('type','')}\n- Points: {x.get('value','')}\n- Challenge ID: {x.get('id','')}\n- Recommended skill: `{family}`\n- Work directory: `work/`\n- Evidence directory: `flag_output_dir/`\n- Writeup: `writeup/solution.md`\n\n## Tools\n\nVerify suitable tools in `{repo_root}/config/tools.json` before use.\n\n## Validation\n\nDo not call a hint, banner, OCR result or unverified string a final flag. Validate against the intended artifact, checker or service and save evidence in `flag_output_dir/`.\n"
        (d/'AGENT.md').write_text(agent)
        risk=[]
        for p in d.iterdir():
            if p.is_file() and p.name not in {'README.md','AGENT.md','EXECUTION-SAFETY.md','attachment-manifest.json'} and (os.access(p,os.X_OK) or p.suffix.lower() in {'.py','.sh','.js','.php','.exe','.dll','.so','.jar','.apk','.class'}): risk.append(f'- `{p.name}`: inspect/run only inside `bin/run-isolated` when untrusted')
        (d/'EXECUTION-SAFETY.md').write_text('# Execution Safety\n\n'+('\n'.join(risk) if risk else 'No obvious executable/script attachment detected.')+'\n')
    (ROOT/'INDEX.md').write_text('\n'.join(index)+'\n')
    # Keep a non-destructive report of files no longer listed by CTFd.
    stale=[]
    generated={'README.md','AGENT.md','EXECUTION-SAFETY.md','attachment-manifest.json','.solver-status','.ctf-profile.json','challenges.json','challenges-detailed.json','_ctf-info.md','INDEX.md','STATUS.md','STALE-FILES.md','CLEANUP-REPORT.md'}
    for item in items:
        d=challenge_dir(item); expected=attachment_names(item)
        if not d.exists(): continue
        for p in d.iterdir():
            if p.is_file() and p.name not in generated and p.name not in {'.pipeline.lock','.gitignore','submit.sh','launch.sh'} and p.name not in expected:
                stale.append(str(p.relative_to(ROOT)))
    (ROOT/'STALE-FILES.md').write_text('# Stale File Report\n\nFiles not currently listed by CTFd are reported only; nothing is deleted.\n\n'+('\n'.join(f'- `{x}`' for x in sorted(stale)) if stale else 'No stale files detected.')+'\n')

def set_status(challenge, value):
    if value not in {'not_started','in_progress','solved'}: raise SystemExit('status must be not_started, in_progress or solved')
    items=load_json(ROOT/'challenges-detailed.json')
    found=[x for x in items if slug(x.get('name',''))==slug(challenge) or str(x.get('id'))==str(challenge)]
    if not found: raise SystemExit('challenge not found')
    d=challenge_dir(found[0]); d.mkdir(parents=True,exist_ok=True); (d/'.solver-status').write_text(value+'\n'); generated_docs(); dashboard(); cleanup_report(); print('Status updated:',found[0].get('name'),value)

def profile_doctor():
    for name in ('challenges-detailed.json','INDEX.md','STATUS.md','FOLDER-RENAME-REPORT.md','.ctf-profile.json'):
        p=ROOT/name; print('[OK]' if p.exists() else '[FAIL]',name)
    for item in load_json(ROOT/'challenges-detailed.json'):
        d=challenge_dir(item); expected=attachment_names(item)
        for name in sorted(expected):
            if not (d/name).exists():
                if (d/(name+'.part')).exists(): print('[WARN] partial attachment',d/(name+'.part'))
                else: print('[WARN] attachment not downloaded',d/name)
        manifest=d/'attachment-manifest.json'
        if manifest.exists():
            recorded={x['file']:x['sha256'] for x in load_json(manifest).get('files',[])}
            for name in expected:
                p=d/name
                if p.exists() and recorded.get(name)!=hashlib.sha256(p.read_bytes()).hexdigest(): print('[WARN] manifest mismatch',p)
    print('Profile doctor complete')

def folder_report():
    items=load_json(ROOT/'challenges-detailed.json'); expected={challenge_dir(x).relative_to(ROOT):x for x in items}; moved=[]; unmatched=[]
    for cat in ROOT.iterdir():
        if not cat.is_dir() or cat.name in {'.ctfd','.pipeline','.history','.git','manual'}: continue
        for d in cat.iterdir():
            if not d.is_dir() or d.relative_to(ROOT) in expected: continue
            readme=d/'README.md'; text=readme.read_text(errors='ignore') if readme.exists() else ''
            m=__import__('re').search(r'^#\s+(.+)$',text,__import__('re').M)
            match=next((x for x in items if m and x.get('name','').strip()==m.group(1).strip()),None)
            if match and not challenge_dir(match).exists():
                target=challenge_dir(match); target.parent.mkdir(parents=True,exist_ok=True); d.rename(target); moved.append(f'{d.relative_to(ROOT)} -> {target.relative_to(ROOT)}')
            else: unmatched.append(str(d.relative_to(ROOT)))
    lines=['# Folder Rename Report','','Folders are never deleted automatically.','','## Matched and moved']+([f'- `{x}`' for x in moved] or ['- None'])+['','## Unmatched folders requiring review']+([f'- `{x}`' for x in unmatched] or ['- None'])
    (ROOT/'FOLDER-RENAME-REPORT.md').write_text('\n'.join(lines)+'\n')

def init_git():
    if not (ROOT/'.git').exists(): os.system(f'git -C {ROOT} init -q')
    p=ROOT/'.gitignore'
    if not p.exists(): p.write_text('.ctfd/config.json\n.ctf-profile.json\nchallenges.json\nchallenges-detailed.json\n.pipeline/\n.history/\n*.log\n')
    print('Git tracking ready:',ROOT)

def dashboard():
    items=load_json(ROOT/'challenges-detailed.json'); rows=[]
    for x in items:
        d=challenge_dir(x); v=(d/'.solver-status').read_text().strip() if (d/'.solver-status').exists() else 'not_started'
        rows.append(f"| { {'not_started':'[ ]','in_progress':'[~]','solved':'[x]'}.get(v,'[ ]') } | {x.get('name','')} | {x.get('category','')} |")
    (ROOT/'STATUS.md').write_text('# Solver Dashboard\n\n| Status | Challenge | Category |\n|---|---|---|\n'+'\n'.join(rows)+'\n')

def cleanup_report():
    (ROOT/'CLEANUP-REPORT.md').write_text('# Cleanup Report\n\nAdvisory only; no files are deleted automatically. Review `.history/`, `STALE-FILES.md`, empty directories and duplicate attachments manually.\n')

def main():
    cmd=sys.argv[1] if len(sys.argv)>1 else 'help'
    if cmd=='snapshot': snapshot()
    elif cmd=='diff': show_diff()
    elif cmd=='dry-run': dry_run()
    elif cmd=='archive': archive()
    elif cmd=='generate': metadata(); generated_docs(); folder_report(); dashboard(); cleanup_report()
    elif cmd=='set-status': set_status(sys.argv[3],sys.argv[4])
    elif cmd=='doctor': profile_doctor()
    elif cmd=='git-init': init_git()
    elif cmd=='open':
        q=sys.argv[3]; found=[x for x in load_json(ROOT/'challenges-detailed.json') if slug(x.get('name',''))==slug(q) or str(x.get('id'))==str(q)]
        if not found: raise SystemExit('challenge not found')
        print(challenge_dir(found[0]))
    else: print('usage: ctf-pipeline.py {snapshot|diff|dry-run|archive|generate|set-status|doctor|git-init|open} ROOT')
if __name__=='__main__': main()
