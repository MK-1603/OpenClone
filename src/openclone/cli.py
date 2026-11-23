"""OpenClone CLI entry point."""
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def main():
    """Main CLI entrypoint for openclone and aisdf commands."""
    installer_verbs = {"install", "uninstall", "doctor", "status", "update", "rollback", "installer"}
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        from src.openclone.mcp.server import main as mcp_main
        mcp_main()
    elif len(sys.argv) > 1 and sys.argv[1] == "lifecycle":
        from tools.checklist_engine import main as lifecycle_main
        sys.argv.pop(1)
        lifecycle_main()
    elif len(sys.argv) > 1 and sys.argv[1] == "skill":
        from tools.skill_engine import main as skill_main
        sys.argv.pop(1)
        skill_main()
    elif len(sys.argv) > 1 and sys.argv[1] in installer_verbs:
        from src.openclone.installer.cli import main as installer_main
        if sys.argv[1] == "installer":
            sys.argv.pop(1)
        installer_main()
    else:
        from runtime.openclone_runtime.workforce import main as workforce_main
        workforce_main()


if __name__ == "__main__":
    main()
