from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from scapy.all import IP, TCP, wrpcap

root = Path('/home/zisec/ctf/test-corpus')
for d in ('pwn', 'rsa', 'apk', 'pcap', 'memory'):
    (root / d).mkdir(parents=True, exist_ok=True)
(root / 'pwn' / 'ret2win.c').write_text('#include <stdio.h>\n#include <unistd.h>\nvoid win(void){puts("TEST_WIN");}\nint main(void){char b[32];read(0,b,128);}\n')
(root / 'rsa' / 'README.txt').write_text('RSA fixture slot for solver smoke tests.\n')
(root / 'memory' / 'synthetic.raw').write_bytes(b'CTF-MEMORY-TEST\x00' + bytes(4096))
with ZipFile(root / 'apk' / 'sample.apk', 'w', ZIP_DEFLATED) as z:
    z.writestr('AndroidManifest.xml', b'<manifest package="ctf.test"/>')
    z.writestr('classes.dex', b'dex\n035\x00' + bytes(100))
wrpcap(str(root / 'pcap' / 'sample.pcap'), [IP(dst='192.0.2.1')/TCP(dport=31337, flags='S'), IP(src='192.0.2.1')/TCP(sport=31337, flags='SA')])
print(root)
