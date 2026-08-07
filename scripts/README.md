# Repository scripts

Portable scripts behind the root `make` interface live here. Scripts must fail clearly, avoid unsafe defaults, and remain usable on supported macOS and Linux environments.

| Script | Responsibility |
|---|---|
| `bootstrap.sh` | Install pinned workspace dependencies, create local configuration, and configure Git hooks |
| `dev.sh` | Validate prerequisites and start the Docker Compose development profile |
| `uv.sh` | Resolve the repository-managed or system `uv` executable consistently |
