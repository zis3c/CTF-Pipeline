# CTF Tool Manifest

Generated inventory of detected system and Python CTF tools. The authoritative machine-readable copy is `../config/tools.json`.

## Pwn

- ROPgadget — on: Gadgets finder for ROP exploitation code | `ROPgadget`
- afl-fuzz — on: instrumentation-driven fuzzer for binary formats | `afl-fuzz`
- checksec — on: Bash script to test executable properties | `checksec`
- gdb — on: GNU Debugger | `gdb`
- gdb-multiarch — on: GNU Debugger (with support for multiple architectures) | `gdb-multiarch`
- pwndbg — Git repository: https://github.com/pwndbg/pwndbg.git | `/usr/local/bin/pwndbg`

## Reverse Engineering

- adb — on: Android Debug Bridge | `adb`
- apktool — on: tool for reverse engineering Android apk files | `apktool`
- d2j-dex2jar — on: Tools to work with android .dex and java .class files | `d2j-dex2jar`
- frida (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida`
- frida-apk (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-apk`
- frida-compile (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-compile`
- frida-create (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-create`
- frida-discover (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-discover`
- frida-itrace (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-itrace`
- frida-join (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-join`
- frida-kill (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-kill`
- frida-ls (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-ls`
- frida-ls-devices (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-ls-devices`
- frida-pm (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-pm`
- frida-ps (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-ps`
- frida-pull (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-pull`
- frida-push (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-push`
- frida-rm (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-rm`
- frida-strace (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-strace`
- frida-trace (package: `frida-tools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/frida-trace`
- ghidraRun — on: Software Reverse Engineering Framework | `ghidraRun`
- jadx — on: Dex to Java decompiler | `jadx`
- objection (package: `objection`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/objection`
- qemu-arm — on: QEMU user mode emulation (static binaries) | `qemu-arm`
- r2 — on: free and advanced command line hexadecimal editor | `r2`
- readpe — on: command-line tools to manipulate Windows PE files | `readpe`
- rz — on: reverse engineering framework and command-line toolset | `rz`
- smali — on: assembler/disassembler for Android's dex format | `smali`

## Crypto

- boolector — on: SMT solver for bit-vectors and arrays | `boolector`
- ecm — on: Factor integers using the Elliptic Curve Method | `ecm`
- gnark — Git repository: https://github.com/Consensys/gnark.git | `/usr/local/bin/gnark`
- gnark-crypto — Git repository: https://github.com/Consensys/gnark-crypto.git | `/usr/local/bin/gnark-crypto`
- gp — on: PARI/GP Computer Algebra System binaries | `gp`
- hashcat — on: World's fastest and most advanced password recovery utility | `hashcat`
- john — on: active password cracking tool | `john`
- msoffcrypto-tool (package: `msoffcrypto-tool`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/msoffcrypto-tool`
- name-that-hash (package: `name-that-hash`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/name-that-hash`
- sage — Full SageMath environment for number theory, elliptic curves, and lattices | `/usr/local/bin/sage`
- xortool (package: `xortool`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/xortool`
- xortool-xor (package: `xortool`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/xortool-xor`
- z3 — Python CLI executable discovered from pipx | `$HOME/.local/bin/z3`

## Forensics

- autopsy — on: graphical interface to SleuthKit | `autopsy`
- binwalk — on: tool library for analyzing binary blobs and executable code | `binwalk`
- capa (package: `flare-capa`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/capa`
- ewfmount — on: collection of tools for reading and writing EWF files | `ewfmount`
- foremost — on: forensic program to recover lost files | `foremost`
- olebrowse (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/olebrowse`
- oledir (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/oledir`
- olefile (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/olefile`
- oleid (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/oleid`
- olemap (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/olemap`
- olemeta (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/olemeta`
- oleobj (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/oleobj`
- oletimes (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/oletimes`
- olevba (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/olevba`
- pngcheck — on: print info and check PNG, JNG and MNG files | `pngcheck`
- pngcrush — on: optimizes PNG (Portable Network Graphics) files | `pngcrush`
- steghide — on: steganography hiding tool | `steghide`
- stegseek — on: Worlds fastest steghide cracker | `stegseek`
- tcpflow — on: TCP flow recorder | `tcpflow`
- trivy — on: comprehensive and versatile security scanner | `trivy`
- tshark — on: network traffic analyzer - console version | `tshark`
- vol — Python CLI executable discovered from pipx | `$HOME/.local/bin/vol`
- volshell — Python CLI executable discovered from pipx | `$HOME/.local/bin/volshell`
- wireshark — on: network traffic analyzer - graphical interface | `wireshark`
- yara — on: Pattern matching swiss knife for malware researchers | `yara`

## Web

- burpsuite — on: platform for security testing of web applications | `burpsuite`
- commix — on: Automated All-in-One OS Command Injection and Exploitation Tool | `commix`
- dirsearch — on: Web path scanner | `dirsearch`
- dnsrecon — on: Powerful DNS enumeration script | `dnsrecon`
- feroxbuster — on: fast, simple, recursive content discovery tool written in Rust | `feroxbuster`
- ffuf — on: Fast web fuzzer written in Go (program) | `ffuf`
- gobuster — on: high-performance discovery tool for directories, DNS and cloud storage | `gobuster`
- naabu — on: fast port scanner with a focus on reliability and simplicity | `naabu`
- nikto — on: web server security scanner | `nikto`
- nuclei — on: Fast and customizable vulnerability scanner based on simple YAML based DSL | `nuclei`
- paramspider (package: `paramspider`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/paramspider`
- sqlmap — on: automatic SQL injection tool | `sqlmap`
- wafw00f — on: identify and fingerprint Web Application Firewall products | `wafw00f`
- wfuzz — on: Web application bruteforcer | `wfuzz`
- xsser — on: XSS testing framework | `xsser`
- zphisher — Git repository: https://github.com/htr-tech/zphisher.git | `/usr/local/bin/zphisher`

## Blockchain / Web3

- anvil — Foundry Ethereum development and CTF interaction tool | `anvil`
- cast — Foundry Ethereum development and CTF interaction tool | `cast`
- chisel — Foundry Ethereum development and CTF interaction tool | `chisel`
- forge — Foundry Ethereum development and CTF interaction tool | `forge`
- slither (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither`
- slither-check-erc (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-check-erc`
- slither-check-kspec (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-check-kspec`
- slither-check-upgradeability (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-check-upgradeability`
- slither-doctor (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-doctor`
- slither-documentation (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-documentation`
- slither-find-paths (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-find-paths`
- slither-flat (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-flat`
- slither-format (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-format`
- slither-interface (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-interface`
- slither-mutate (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-mutate`
- slither-prop (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-prop`
- slither-read-storage (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-read-storage`
- slither-simil (package: `slither-analyzer`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/slither-simil`
- web3.py — Python Web3/Ethereum interaction library in an isolated environment | `/opt/blockchain-python/bin/python -c 'from web3 import Web3'`

## Misc / OSINT

- aircrack-ng — on: wireless WEP/WPA cracking utilities | `aircrack-ng`
- amass — on: In-depth DNS Enumeration and Network Mapping | `amass`
- bCNC (package: `bcnc`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/bCNC`
- boo (package: `boofuzz`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/boo`
- evil-winrm — on: ultimate WinRM shell for hacking/pentesting | `evil-winrm`
- ezhexviewer (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/ezhexviewer`
- fdfind — on: Simple, fast and user-friendly alternative to find | `fdfind`
- ffmpeg — on: Tools for transcoding, streaming and playing of multimedia files | `ffmpeg`
- flask-unsign — Python CLI executable discovered from pipx | `$HOME/.local/bin/flask-unsign`
- ftguess (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/ftguess`
- fzf — on: general-purpose command-line fuzzy finder | `fzf`
- grgsm — on: GNU Radio blocks and tools for receiving GSM transmissions | `grgsm`
- hackrf_info — on: Software defined radio peripheral - utilities | `hackrf_info`
- hydra — on: very fast network logon cracker | `hydra`
- impacket — on: Links to useful impacket scripts examples | `impacket`
- kismet — on: wireless network and device detector (metapackage) | `kismet`
- minimodem — on: general-purpose software audio FSK modem | `minimodem`
- mraptor (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/mraptor`
- msfconsole — on: Framework for exploit development and vulnerability research | `msfconsole`
- msodde (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/msodde`
- multimon-ng — on: digital radio transmission decoder | `multimon-ng`
- ncat — on: NMAP netcat reimplementation | `ncat`
- nmap — on: The Network Mapper | `nmap`
- nth (package: `name-that-hash`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/nth`
- parallel — on: build and execute command lines from standard input in parallel | `parallel`
- pcodedmp (package: `pcodedmp`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/pcodedmp`
- pytesseract (package: `pytesseract`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/pytesseract`
- pyxswf (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/pyxswf`
- rg — on: Recursively searches directories for a regex pattern | `rg`
- rtfobj (package: `oletools`) — Python CLI executable discovered from pipx | `$HOME/.local/bin/rtfobj`
- rustscan — on: Modern Port Scanner | `rustscan`
- sox — on: Swiss army knife of sound processing | `sox`
- spike — on: Network protocol fuzzer | `spike`
- terraform — on: tool for building, changing, and versioning infrastructure | `terraform`
- tiff2fsspec — Python CLI executable discovered from pipx | `$HOME/.local/bin/tiff2fsspec`
- tiffcomment — Python CLI executable discovered from pipx | `$HOME/.local/bin/tiffcomment`
- tifffile — Python CLI executable discovered from pipx | `$HOME/.local/bin/tifffile`
- yq — on: Command-line YAML processor - jq wrapper for YAML documents | `yq`
- ysoserial — Python CLI executable discovered from pipx | `$HOME/.local/bin/ysoserial`
- zzuf — on: transparent application fuzzer | `zzuf`

## General / AI Agent

- Google-Form-Spammer — General/AI-agent repository: https://github.com/zis3c/Google-Form-Spammer.git | `python3 /usr/local/bin/google-form-spammer`
- Osintgram — General/AI-agent repository: https://github.com/Datalux/Osintgram.git | `python3 /usr/local/bin/osintgram`
- phoneinfoga — General/AI-agent repository: https://github.com/sundowndev/phoneinfoga.git | `/opt/general-tools/phoneinfoga`
- sherlock — General/AI-agent repository: https://github.com/sherlock-project/sherlock.git | `/opt/general-tools/sherlock`
