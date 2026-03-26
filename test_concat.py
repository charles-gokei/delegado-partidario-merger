import unittest
import subprocess
import sys
import tempfile
import csv
from pathlib import Path


def _write_csv(path, header, rows):
    path = Path(path)
    with path.open("w", encoding="latin1", newline='') as f:
        f.write(','.join(header) + "\n")
        for r in rows:
            f.write(','.join(r) + "\n")


class ConcatScriptTest(unittest.TestCase):
    """Functional test using unittest: run concat.py in an isolated tmp dir and
    assert the produced delegado_partidario.csv contains the combined rows.
    """

    def test_concat_creates_combined_csv(self):
        header = ["col1", "col2"]
        rows1 = [["a", "1"], ["b", "2"]]
        rows2 = [["c", "3"]]

        with tempfile.TemporaryDirectory() as tmpdir:
            p1 = Path(tmpdir) / "a.csv"
            p2 = Path(tmpdir) / "b.csv"
            _write_csv(p1, header, rows1)
            _write_csv(p2, header, rows2)

            script_path = Path(__file__).parent / "concat.py"
            self.assertTrue(script_path.exists(),
                            f"concat.py not found at {script_path}")

            subprocess.run([sys.executable, str(script_path)],
                           cwd=tmpdir, check=True)

            out = Path(tmpdir) / "delegado_partidario.csv"
            self.assertTrue(
                out.exists(), "Output file delegado_partidario.csv was not created")

            with out.open("r", encoding="latin1", newline='') as f:
                reader = csv.reader(f, delimiter=',')
                rows = list(reader)

            self.assertEqual(rows[0], header)
            self.assertEqual(rows[1:], rows1 + rows2)


if __name__ == "__main__":
    unittest.main()
