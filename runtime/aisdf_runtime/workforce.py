"""Backward-compatibility wrapper for openclone_runtime.workforce."""
from runtime.openclone_runtime.workforce import *
from runtime.openclone_runtime.workforce import main, OpenCloneError, AisdfError

if __name__ == "__main__":
    main()
