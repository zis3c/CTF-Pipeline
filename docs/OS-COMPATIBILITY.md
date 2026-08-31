# OS Compatibility

## Support matrix

| OS | Level | Required adjustments |
|---|---|---|
| Kali Linux amd64 | Full | Reference development platform. |
| Debian/Ubuntu amd64 | Supported | Install Bash, Python 3.12, Git, Podman and CTF tools yourself. |
| Debian-based ARM64 | Best effort | Some native binaries and reverse-engineering tools may not be available. |
| WSL2 | Best effort | Configure networking, Podman, GUI/browser integration and Linux permissions. |
| macOS | Experimental | Replace Linux paths, `apt` assumptions and container setup. |
| Windows native | Unsupported | Use WSL2 or a Linux virtual machine. |

## Portability limitations

The pipeline uses Bash, GNU utilities, Linux permissions and Python 3.12. Repository paths are derived from the checkout location and can be overridden with `CTF_HOME`; Python can be selected with `CTF_PYTHON`. It is designed for Kali Linux and Debian-based Linux systems. Windows and macOS are not first-class targets because the synchronization CLI, file permissions and several CTF tools are Linux-oriented.

## CTFd compatibility

The pipeline targets standard CTFd API endpoints and the `ctfd-player-cli` behavior documented by its upstream project. Custom authentication, WAF behavior, non-standard attachment endpoints and servers without HTTP Range support may require fallback handling. Use `--dry-run` and the integration fixture before trusting a new deployment.
