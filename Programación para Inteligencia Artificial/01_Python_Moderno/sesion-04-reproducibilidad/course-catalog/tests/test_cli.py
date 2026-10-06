import subprocess
import sys
from pathlib import Path

MAIN = Path(__file__).resolve().parents[1] / "main.py"


def test_missing_catalog_exits_with_error(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    result = subprocess.run(
        [sys.executable, str(MAIN), "python", "--catalog", str(missing)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Catalog search failed" in result.stderr
