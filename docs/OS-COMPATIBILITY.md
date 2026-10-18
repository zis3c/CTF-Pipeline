# OS Compatibility

## Support matrix

| OS | Level | Required adjustments |
|---|---|---|
| Kali Linux amd64 | Full | Reference development platform. |
| Debian/Ubuntu amd64 | Supported | Install Bash, Python 3.10+, Git, Podman and CTF tools yourself. |
| Debian-based ARM64 | Best effort | Some native binaries and reverse-engineering tools may not be available. |
| WSL2 | Supported | Run the Linux scripts. Configure networking, Podman and GUI/browser integration as needed. |
| Windows native | Supported | Use the PowerShell scripts; see [`WINDOWS.md`](WINDOWS.md). Linux permissions, `apt`/`gem` and Podman isolation do not apply. |

macOS is out of scope. The Bash scripts rely on GNU utilities, `apt`/`gem` package names and Linux permissions that macOS does not provide.

## Portability limitations

The pipeline uses Bash, GNU utilities, Linux permissions and Python 3.10+. Repository paths are derived from the checkout location and can be overridden with `CTF_HOME`; Python can be selected with `CTF_PYTHON`. It is designed for Kali Linux and Debian-based Linux systems. On native Windows the Bash scripts are mirrored by PowerShell ports (`bin\*.ps1`, `config\activate-ctf.ps1`): Linux permissions are skipped, tool installation uses pip instead of apt, and isolation uses Docker/Podman or Windows Sandbox. Several CTF tools remain Linux-oriented, so Windows is a supported but reduced target.

## CTFd compatibility

The pipeline targets standard CTFd API endpoints and the bundled `ctfd` client. Custom authentication, WAF behavior and non-standard attachment endpoints may require fallback handling; the client falls back from token auth to username/password session login. Use `--dry-run` and the integration fixture before trusting a new deployment.
