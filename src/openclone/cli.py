"""OpenClone CLI entry point."""
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def main():
    """Main CLI entrypoint for openclone and aisdf commands."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-v", "version"):
        try:
            from src.openclone import __version__
            print(f"openclone {__version__}")
        except Exception:
            print("openclone 1.0.0")
        return

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
    elif len(sys.argv) > 1 and sys.argv[1] in ("intelligence", "intel"):
        from src.openclone.intelligence.cli import main as intel_main
        sys.argv.pop(1)
        intel_main()
    elif len(sys.argv) > 1 and sys.argv[1] == "agency":
        from src.openclone.workforce.agency.cli import main as agency_main
        sys.argv.pop(1)
        agency_main()
    elif len(sys.argv) > 1 and sys.argv[1] == "brand":
        from src.openclone.branding.cli import main as brand_main
        sys.argv.pop(1)
        brand_main()
    elif len(sys.argv) > 1 and sys.argv[1] in installer_verbs:
        from src.openclone.installer.cli import main as installer_main
        if sys.argv[1] == "installer":
            sys.argv.pop(1)
        installer_main()
    else:
        from src.openclone.runtime.workforce import main as workforce_main
        workforce_main()


if __name__ == "__main__":
    main()
