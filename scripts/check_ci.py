"""Run the CausalIQ quality gates.

This is the canonical entry point for the umbrella repository; generated
package copies vendor ``causaliq_devtools`` instead of importing this package.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causaliq.devtools.gate import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
