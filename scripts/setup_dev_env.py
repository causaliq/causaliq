# generated from causaliq@693e2bfe00df-dirty src/causaliq/devtools/templates.py - do not edit
"""Create and verify the shared CausalIQ environments."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causaliq.devtools.devenv import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
