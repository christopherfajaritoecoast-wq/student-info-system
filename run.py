"""Launcher: run the application from the project root with `python run.py`."""

import sys
from pathlib import Path

# Make sure `src` can be imported no matter where the script is started from.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
