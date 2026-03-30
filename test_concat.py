import unittest
import subprocess
import sys
import tempfile
import csv
from pathlib import Path


def _write_csv(path, header, rows, sep=";"):
    path = Path(path)
    with path.open("w", encoding="latin1", newline='') as f:
        f.write(sep.join(header) + "\n")
        for r in rows:
            f.write(sep.join(r) + "\n")


class ConcatScriptTest(unittest.TestCase):
    # Test data constants
    CSV_HEADER = ["col1", "col2"]
    CSV_ROWS_1 = [["a", "1"], ["b", "2"]]
    CSV_ROWS_2 = [["c", "3"]]
    OUTPUT_FILENAME = "delegado_partidario.csv"
    SCRIPT_FILENAME = "concat.py"

    """Functional test using unittest: run concat.py in an isolated tmp dir and
    assert the produced delegado_partidario.csv contains the combined rows.
    """

    def test_concat_creates_combined_csv(self):

        with tempfile.TemporaryDirectory() as tmpdir:

            self._create_tests_csvs(tmpdir)

            script_path = self._get_script_path()

            self._run_concat_script(tmpdir, script_path)

            out = Path(tmpdir) / "delegado_partidario.csv"
            self.assertTrue(
                out.exists(), "Output file delegado_partidario.csv was not created")

            with out.open("r", encoding="latin1", newline='') as f:
                reader = csv.reader(f, delimiter=';')
                rows = list(reader)

            self.assertEqual(rows[0], self.CSV_HEADER)
            self.assertEqual(rows[1:], self.CSV_ROWS_1 + self.CSV_ROWS_2)

    def _create_tests_csvs(self, tmpdir):
        """Create csv files in tmp directory"""
        p1 = Path(tmpdir) / "a.csv"
        p2 = Path(tmpdir) / "b.csv"
        _write_csv(p1, self.CSV_HEADER, self.CSV_ROWS_1)
        _write_csv(p2, self.CSV_HEADER, self.CSV_ROWS_2)

    def _run_concat_script(self, tmpdir, script_path):
        subprocess.run([sys.executable, str(script_path)],
                       cwd=tmpdir, check=True)

    def _get_script_path(self):
        """Get the path to concat.py script"""
        script_path = Path(__file__).parent / "concat.py"
        self.assertTrue(script_path.exists(),
                        f"concat.py not found at {script_path}")
        return script_path


if __name__ == "__main__":
    unittest.main()
