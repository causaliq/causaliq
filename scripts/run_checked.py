"""Launch a command and observe completion through its exit artefact."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causaliq.devtools.run_checked import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
