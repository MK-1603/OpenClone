"""OpenClone CLI entry point."""
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        from src.openclone.mcp.server import main
        main()
    else:
        from runtime.aisdf_runtime.workforce import main
        main()
