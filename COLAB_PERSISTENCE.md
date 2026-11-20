# Colab workspace persistence

Workspace: `/content/persistent-mcp-server`  
Drive backups: `My Drive/ChatGPT-Workspace/`

## Start / recover
Open `Start_ChatGPT_Workspace.ipynb` from the Drive folder and run all cells. It mounts Drive, restores the newest SHA-256-verified archive (falling back to an older valid archive), checks system health, and starts automatic checkpointing.

## Normal use
- Automatic checkpoints: every 5 minutes and after successful notebook cells (90-second debounce).
- Manual checkpoint: `python /content/persistent-mcp-server/workspace_manager.py save`
- Status: `python /content/persistent-mcp-server/workspace_manager.py status`
- Restore: `python /content/persistent-mcp-server/workspace_manager.py restore` (verifies SHA-256 and archive paths before extraction).
- Optional public preview: enable the final notebook cell. Cloudflare quick-tunnel URLs are temporary.

## Backup policy
The manager retains the latest 10 timestamped archives and manifests. It excludes `.git`, caches, virtual environments, credential files, `.pem`, and `.key` files. The recovery notebook and helper copies are stored separately in Drive.

## Limits
Colab runtimes are temporary and subject to Google capacity and usage limits. No code runs while a runtime is stopped. Drive preserves files, not live processes or credentials. Secrets must be reconnected securely.
