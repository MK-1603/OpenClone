# Update and Lifecycle Architecture — OpenClone
## Atomic Updates, Release Channels & Rollback Recovery

**Canonical Package:** `openclone`  
**Primary CLI:** `openclone`  
**Legacy Alias:** `aisdf`  
**Version:** 1.0.0  
**Status:** `SPECIFIED & IN_IMPLEMENTATION`  

---

## 1. Overview & Update Philosophy

The OpenClone update engine provides safe, verifiable, and atomic updates. It prevents broken installations, partial overwrites, and accidental downgrades by enforcing:
1. **Cryptographic Integrity:** Downloaded update artifacts are validated against SHA-256 hashes declared in signed release manifests.
2. **Transactional Staging:** Updates are downloaded and extracted into isolated staging directories; active binaries are never overwritten in-place until pre-flight checks pass.
3. **Pre-Update Snapshots:** Current binaries and configurations are snapshotted prior to applying changes.
4. **Automated Rollback:** If health checks (`openclone doctor`) fail on the newly staged binary, the transaction is automatically aborted and the previous state is restored.
5. **Installation Ownership Respect:** Updates are routed through the native mechanism that originally installed the platform (e.g. `pip install --upgrade openclone` if installed via pip).

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant CLI as OpenClone CLI
    participant UE as UpdateEngine
    participant API as Release API / PyPI
    participant RM as RollbackManager
    participant FS as Local Filesystem

    User->>CLI: openclone update check
    CLI->>UE: Discover latest release (channel)
    UE->>API: Fetch release-manifest.json
    API-->>UE: Manifest (version, SHA-256, compatibility)
    UE-->>CLI: Update Available: v1.1.0 (Current: v1.0.0)
    
    User->>CLI: openclone update apply
    CLI->>UE: Start update transaction
    UE->>UE: Verify compatibility (OS, Arch, Python)
    UE->>API: Download artifact to staging directory
    UE->>UE: Verify SHA-256 checksum
    UE->>RM: Snapshot current installation state
    RM->>FS: Create backup snapshot (.bak-<timestamp>)
    UE->>FS: Apply update into installation target
    UE->>CLI: Run diagnostic health check (doctor)
    alt Health Check Passes
        CLI->>UE: Health check PASS (5/5)
        UE->>RM: Commit transaction
        UE-->>User: Successfully updated to v1.1.0
    else Health Check Fails
        CLI->>UE: Health check FAIL
        UE->>RM: Trigger automatic rollback
        RM->>FS: Restore snapshot from .bak
        UE-->>User: Update aborted; previous version restored safely
    end
```

---

## 2. Release Channels

OpenClone supports three distinct release channels:

| Channel | Cadence | Intended Audience | Stability Guarantee |
|---|---|---|---|
| **`stable`** (Default) | Monthly / Patch as needed | Production teams, enterprise environments | Fully verified, 100% test pass, no breaking API changes |
| **`beta`** | Bi-weekly | Early adopters, integration partners | Feature complete; may contain minor experimental warnings |
| **`nightly`** | Continuous | Framework maintainers, automated regression testers | Built from latest `main` commit; potential instability |

Channel configuration is managed via:
```bash
openclone update channel --set stable
openclone update channel --show
```

---

## 3. Release Manifest Contract

Every release publishes a cryptographic manifest conforming to `framework/schemas/release-manifest.schema.json`:

```json
{
  "product": "openclone",
  "version": "1.0.0",
  "channel": "stable",
  "published_at": "2026-11-25T11:00:00Z",
  "min_python_version": "3.10.0",
  "artifacts": [
    {
      "filename": "openclone-1.0.0-py3-none-any.whl",
      "os": "any",
      "arch": "any",
      "distribution_type": "wheel",
      "size_bytes": 298412,
      "sha256": "10611d0e000c9e010eb1c25f3e56f9edf6ca85ce8ecff6f35d1d2f7e20603465",
      "url": "https://github.com/MK-1603/OpenClone/releases/download/v1.0.0/openclone-1.0.0-py3-none-any.whl"
    },
    {
      "filename": "OpenClone-Setup-v1.0.0.exe",
      "os": "windows",
      "arch": "x64",
      "distribution_type": "windows-installer",
      "size_bytes": 18451920,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "url": "https://github.com/MK-1603/OpenClone/releases/download/v1.0.0/OpenClone-Setup-v1.0.0.exe"
    }
  ],
  "required_migrations": []
}
```

---

## 4. Rollback & State Restoration Engine

The `RollbackManager` enforces state separation:
1. **Application Binaries:** Backed up to `~/.openclone/backups/binaries/<version>-<timestamp>/`.
2. **User Configuration:** Backed up to `~/.openclone/backups/config/<version>-<timestamp>/`.
3. **User Projects & Data:** Never modified during platform updates.

### Manual Rollback:
If a user wishes to revert an applied update:
```bash
openclone update rollback
```
The RollbackManager locates the most recent snapshot, verifies its SHA-256 integrity, replaces the active binaries, verifies configuration compatibility, and executes a health check.
