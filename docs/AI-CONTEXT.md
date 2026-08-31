# AI Context Guide

Read `$CTF_HOME/README.md`, run `ctf-pull list`, then select one `ctfs/<profile>/` and read its `challenges-detailed.json` and challenge README. Never mix profiles. Work only inside that challenge's `work/`; put reasoning in `notes/`, final text in `writeup/solution.md`, and validated evidence in `flag_output_dir/`.

Read the challenge `AGENT.md` for category, ID, paths and validation rules. Use `attachment-manifest.json` to confirm artifact hashes and `EXECUTION-SAFETY.md` before running files. Use `INDEX.md` and `.solver-status` to understand progress.

Route web/API to web, native binary to reverse then pwn, mathematics to crypto, disk/memory/PCAP/stego to forensics, APK/WASM to reverse, OSINT to OSINT, and hybrids to misc. Validate flags against the intended artifact, checker or service; hints, banners, OCR and unverified strings are not final flags.
