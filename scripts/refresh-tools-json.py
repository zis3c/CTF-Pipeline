#!/usr/bin/env python3
import json, os, re, subprocess
from pathlib import Path

p = Path(os.environ.get('CTF_HOME', Path(__file__).resolve().parents[1])) / 'config' / 'tools.json'
data = json.loads(p.read_text())
safe_commands = {
    'go', 'rustc', 'cargo', 'gdb', 'nmap', 'curl', 'jq', 'ffuf', 'tshark',
    'binwalk', 'exiftool', 'steghide', 'pycdc', 'vol', 'one_gadget',
    'seccomp-tools', 'zsteg', 'angr', 'uncompyle6', 'ROPgadget', 'ropper'
}
for item in data:
    if 'version' in item:
        continue
    path = Path(item.get('path', ''))
    if item.get('package') and path.exists():
        for candidate in (path.parent / 'python', path.parent.parent / 'bin' / 'python'):
            if candidate.exists():
                try:
                    v = subprocess.run(
                        [str(candidate), '-c',
                         'import importlib.metadata as m; print(m.version('
                         + repr(item['package']) + '))'],
                        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                        timeout=3).stdout.strip()
                    if v:
                        item['version'] = v
                        break
                except Exception:
                    pass
    if 'version' in item:
        continue
    if item.get('install_method') == 'apt' and path.exists():
        try:
            owner = subprocess.run(['dpkg-query', '-S', str(path)], text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   timeout=2).stdout.split(':', 1)[0]
            if owner:
                v = subprocess.run(['dpkg-query', '-W', '-f=' + '$' + '{Version}', owner],
                                   text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, timeout=2).stdout.strip()
                if v:
                    item['version'] = v
        except Exception:
            pass
    if 'version' in item:
        continue
    if path.is_dir() and (path / '.git').exists():
        try:
            v = subprocess.run(['git', '-C', str(path), 'rev-parse', '--short', 'HEAD'],
                               text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=2).stdout.strip()
            if v:
                item['version'] = 'git-' + v
        except Exception:
            pass
    if 'version' in item:
        continue
    invoke = item.get('invoke', '').split()
    if not invoke or not item.get('path') or not os.path.exists(item['path']):
        item['version'] = 'unknown'
        continue
    if Path(invoke[0]).name not in safe_commands:
        item['version'] = 'unknown'
        continue
    try:
        out = subprocess.run(invoke + ['--version'], text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=4).stdout.splitlines()
    except Exception:
        continue
    if out:
        m = re.search(r'(?<!\d)(\d+\.\d+(?:\.\d+)?(?:[-+][\w.]+)?)', out[0])
        if m:
            item['version'] = m.group(1)
    if 'version' not in item:
        item['version'] = 'unknown'
p.write_text(json.dumps(data, indent=2) + '\n')
print(f'refreshed {len(data)} records; versioned {sum("version" in x for x in data)}')
