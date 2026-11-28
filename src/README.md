# OpenClone Source Package Directory

This directory contains the Python package root for OpenClone (`openclone`).

- `openclone/__init__.py`: Package initialization and version definition.
- `openclone/cli.py`: Standalone CLI launcher wrapping the deterministic control plane.

When installing via pip or development editable mode:
```bash
pip install -e .
openclone --help
```
