from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, shutil, tarfile, tempfile
from pathlib import Path

DEFAULT_WORKSPACE = Path("/content/persistent-mcp-server")
DEFAULT_BACKUP_ROOT = Path("/content/drive/MyDrive/ChatGPT-Workspace")
EXCLUDES = {".git", "__pycache__", ".ipynb_checkpoints", "node_modules", ".venv", "venv", ".cache"}
SECRET_HINTS = {"credentials.json", "token.json", ".env", "secrets.json", "service-account.json"}

def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")

def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in EXCLUDES for part in rel.parts):
            continue
        if p.name.lower() in SECRET_HINTS or p.name.lower().endswith((".pem", ".key")):
            continue
        yield p

def drive_ready(backup_root: Path):
    drive_root = Path('/content/drive/MyDrive')
    if not drive_root.is_dir():
        raise SystemExit(
            "Google Drive is not mounted. In a Colab cell run:\n"
            "from google.colab import drive; drive.mount('/content/drive')\n"
            "Then rerun this command."
        )
    if not os.access(drive_root, os.W_OK):
        raise SystemExit("Google Drive is not writable. Reconnect Drive in Colab.")

def checkpoint(workspace: Path, backup_root: Path, keep: int):
    if not workspace.is_dir():
        raise SystemExit(f"Workspace not found: {workspace}")
    drive_ready(backup_root)
    backup_root.mkdir(parents=True, exist_ok=True)
    stamp = now()
    archive = backup_root / f"workspace-{stamp}.tar.gz"
    fd, tmp_name = tempfile.mkstemp(prefix=".checkpoint-", suffix=".tar.gz", dir=backup_root)
    os.close(fd)
    tmp = Path(tmp_name)
    manifest = {"created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                "workspace": str(workspace), "archive": archive.name, "files": []}
    try:
        with tarfile.open(tmp, "w:gz") as tar:
            for p in safe_files(workspace):
                rel = p.relative_to(workspace)
                tar.add(p, arcname=str(rel), recursive=False)
                manifest["files"].append({"path": str(rel), "size": p.stat().st_size, "sha256": sha256(p)})
        os.replace(tmp, archive)
        manifest["archive_sha256"] = sha256(archive)
        mpath = backup_root / f"workspace-{stamp}.json"
        mtmp = mpath.with_suffix(".json.tmp")
        mtmp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        os.replace(mtmp, mpath)
    finally:
        if tmp.exists(): tmp.unlink()
    archives = sorted(backup_root.glob("workspace-*.tar.gz"))
    for old in archives[:-keep] if keep > 0 else []:
        old.unlink(missing_ok=True)
        Path(str(old)[:-7] + ".json").unlink(missing_ok=True)
    print(f"CHECKPOINT_OK {archive}")
    print(f"FILES_SAVED {len(manifest['files'])}")
    print(f"ARCHIVE_SHA256 {manifest['archive_sha256']}")

def restore(workspace: Path, backup_root: Path):
    drive_ready(backup_root)
    archives = sorted(backup_root.glob("workspace-*.tar.gz"), reverse=True)
    if not archives:
        raise SystemExit(f"No checkpoints found in {backup_root}")
    for archive in archives:
        manifest_path = Path(str(archive)[:-7] + ".json")
        if not manifest_path.is_file():
            print(f"SKIP {archive.name}: manifest missing")
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if sha256(archive) != manifest.get("archive_sha256"):
                print(f"SKIP {archive.name}: SHA-256 mismatch")
                continue
            with tarfile.open(archive, "r:gz") as tar:
                base = workspace.resolve()
                members = tar.getmembers()
                safe = True
                for member in members:
                    target = (workspace / member.name).resolve()
                    if target != base and base not in target.parents:
                        safe = False
                    if member.issym() or member.islnk() or member.isdev():
                        safe = False
                if not safe:
                    print(f"SKIP {archive.name}: unsafe archive contents")
                    continue
                workspace.mkdir(parents=True, exist_ok=True)
                tar.extractall(workspace)
            print(f"RESTORE_OK {archive}")
            print(f"WORKSPACE {workspace}")
            return
        except (OSError, ValueError, tarfile.TarError, json.JSONDecodeError) as exc:
            print(f"SKIP {archive.name}: {type(exc).__name__}: {exc}")
    raise SystemExit("No valid checkpoint could be restored; workspace left untouched.")

def status(workspace: Path, backup_root: Path):
    print("WORKSPACE", workspace, "exists=", workspace.is_dir())
    if backup_root.exists():
        archives = sorted(backup_root.glob("workspace-*.tar.gz"))
        print("DRIVE_BACKUP_FOLDER", backup_root)
        print("CHECKPOINTS", len(archives))
        if archives: print("LATEST", archives[-1].name, "bytes=", archives[-1].stat().st_size)
    else:
        print("DRIVE_NOT_MOUNTED_OR_FOLDER_MISSING", backup_root)

def main():
    ap = argparse.ArgumentParser(description="Checkpoint and restore a Colab workspace to Google Drive.")
    ap.add_argument("action", choices=["save", "restore", "status"])
    ap.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    ap.add_argument("--backup-root", type=Path, default=DEFAULT_BACKUP_ROOT)
    ap.add_argument("--keep", type=int, default=10)
    a = ap.parse_args()
    if a.action == "save": checkpoint(a.workspace, a.backup_root, a.keep)
    elif a.action == "restore": restore(a.workspace, a.backup_root)
    else: status(a.workspace, a.backup_root)

if __name__ == "__main__":
    main()
