# Test File Refactoring Instructions

## Overview
This document provides detailed step-by-step instructions to refactor `test_concat.py` for improved legibility and organization.

## Current State Issues
1. Test data (header, rows) is scattered inside the test method
2. Commented-out code clutters lines 22-29
3. Setup, execution, and assertions are not clearly separated
4. File path/name logic is repeated inline

## Refactoring Steps

### Step 1: Add Class-Level Constants
Add these constants at the beginning of the `ConcatScriptTest` class (after the docstring):

```python
    # Test data constants
    CSV_HEADER = ["col1", "col2"]
    CSV_ROWS_1 = [["a", "1"], ["b", "2"]]
    CSV_ROWS_2 = [["c", "3"]]
    OUTPUT_FILENAME = "delegado_partidario.csv"
    SCRIPT_FILENAME = "concat.py"
```

**Benefits:**
- Easy to find and modify test data
- Single source of truth for expected values
- Follows DRY principle

---

### Step 2: Create Helper Method - `_get_script_path()`
Add this method to the class:

```python
    def _get_script_path(self):
        """Get the path to concat.py script."""
        script_path = Path(__file__).parent / self.SCRIPT_FILENAME
        self.assertTrue(script_path.exists(),
                        f"{self.SCRIPT_FILENAME} not found at {script_path}")
        return script_path
```

**Benefits:**
- Encapsulates script path logic
- Easy to reuse in other tests
- Self-documenting method name

---

### Step 3: Create Helper Method - `_create_test_csvs()`
Add this method to the class:

```python
    def _create_test_csvs(self, tmpdir):
        """Create test CSV files in the temporary directory."""
        p1 = Path(tmpdir) / "a.csv"
        p2 = Path(tmpdir) / "b.csv"
        _write_csv(p1, self.CSV_HEADER, self.CSV_ROWS_1)
        _write_csv(p2, self.CSV_HEADER, self.CSV_ROWS_2)
```

**Benefits:**
- Separates setup logic from test logic
- Reduces clutter in test method
- Reusable if you add more tests

---

### Step 4: Create Helper Method - `_run_concat_script()`
Add this method to the class:

```python
    def _run_concat_script(self, tmpdir, script_path):
        """Execute the concat.py script in the given directory."""
        subprocess.run([sys.executable, str(script_path)],
                       cwd=tmpdir, check=True)
```

**Benefits:**
- Isolates subprocess execution logic
- Makes test method more readable
- Easy to modify how the script is called

---

### Step 5: Create Helper Method - `_read_output_csv()`
Add this method to the class:

```python
    def _read_output_csv(self, tmpdir):
        """Read and return the combined CSV output file."""
        out = Path(tmpdir) / self.OUTPUT_FILENAME
        self.assertTrue(out.exists(),
                        f"Output file {self.OUTPUT_FILENAME} was not created")

        with out.open("r", encoding="latin1", newline='') as f:
            reader = csv.reader(f, delimiter=';')
            return list(reader)
```

**Benefits:**
- Encapsulates file reading and validation
- Returns clean data structure
- Reduces test method complexity

---

### Step 6: Refactor `test_concat_creates_combined_csv()`
Replace the entire test method with:

```python
    def test_concat_creates_combined_csv(self):
        """Test that concat.py correctly combines multiple CSV files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup: Create test input files
            self._create_test_csvs(tmpdir)
            script_path = self._get_script_path()

            # Execute: Run the concat script
            self._run_concat_script(tmpdir, script_path)

            # Assert: Verify output contains combined rows
            rows = self._read_output_csv(tmpdir)
            self.assertEqual(rows[0], self.CSV_HEADER)
            self.assertEqual(rows[1:], self.CSV_ROWS_1 + self.CSV_ROWS_2)
```

**Benefits:**
- Clear three-phase structure: Setup → Execute → Assert
- Self-documenting with inline comments
- Much easier to understand test flow
- Reduced method length (from ~28 lines to ~15 lines)

---

### Step 7: Remove Dead Code
Delete lines 22-29 (the commented-out `setUpClass` and `writeDummyCsv` code):

```python
    # def setUpClass(self):
    #     with tempfile.TemporaryDirectory() as tmpdir:
    #         p1 = Path(tmpdir) / ''
    #
    # def writeDummyCsv(tmpdir):
    #     header = ["col1", "col2"]
    #     rows1 = [["a", "1"], ["b", "2"]]
    #     rows2 = [["c", "3"]]
```

**Benefits:**
- Removes clutter and confusion
- Makes file smaller and cleaner
- No functionality lost (code wasn't being used)

---

## Final Result

The refactored file will have:
✅ Clear organization with constants, helper methods, and test method  
✅ Easy-to-find test data  
✅ Reusable helper methods  
✅ Clear Setup → Execute → Assert pattern  
✅ No dead code  
✅ Self-documenting method names and comments  
✅ Same functionality, better readability  

## Verification

After refactoring, run the tests to ensure nothing broke:

```bash
python -m pytest test_concat.py -v
# or
python -m unittest test_concat.py
```

Expected output: **Test passes** with the same assertions as before.

---

## ✅ IMPLEMENTATION COMPLETED

All refactoring steps have been successfully applied to `test_concat.py`.

### Changes Made:

**1. Class Constants Added (Lines 22-26)**
```python
CSV_HEADER = ["col1", "col2"]
CSV_ROWS_1 = [["a", "1"], ["b", "2"]]
CSV_ROWS_2 = [["c", "3"]]
OUTPUT_FILENAME = "delegado_partidario.csv"
SCRIPT_FILENAME = "concat.py"
```
- Test data now lives at the top of the class
- Easy to find and modify
- Single source of truth for expected values

**2. Helper Method `_get_script_path()` Added (Lines 28-33)**
```python
def _get_script_path(self):
    """Get the path to concat.py script."""
    script_path = Path(__file__).parent / self.SCRIPT_FILENAME
    self.assertTrue(script_path.exists(),
                    f"{self.SCRIPT_FILENAME} not found at {script_path}")
    return script_path
```
- Encapsulates script path logic
- Reusable across multiple tests

**3. Helper Method `_create_test_csvs()` Added (Lines 35-40)**
```python
def _create_test_csvs(self, tmpdir):
    """Create test CSV files in the temporary directory."""
    p1 = Path(tmpdir) / "a.csv"
    p2 = Path(tmpdir) / "b.csv"
    _write_csv(p1, self.CSV_HEADER, self.CSV_ROWS_1)
    _write_csv(p2, self.CSV_HEADER, self.CSV_ROWS_2)
```
- Separates setup logic from test method
- Reduces clutter in main test
- Easily extensible

**4. Helper Method `_run_concat_script()` Added (Lines 42-45)**
```python
def _run_concat_script(self, tmpdir, script_path):
    """Execute the concat.py script in the given directory."""
    subprocess.run([sys.executable, str(script_path)],
                   cwd=tmpdir, check=True)
```
- Isolates subprocess execution
- Easier to modify script invocation if needed

**5. Helper Method `_read_output_csv()` Added (Lines 47-55)**
```python
def _read_output_csv(self, tmpdir):
    """Read and return the combined CSV output file."""
    out = Path(tmpdir) / self.OUTPUT_FILENAME
    self.assertTrue(out.exists(),
                    f"Output file {self.OUTPUT_FILENAME} was not created")

    with out.open("r", encoding="latin1", newline='') as f:
        reader = csv.reader(f, delimiter=';')
        return list(reader)
```
- Encapsulates file reading and validation
- Returns clean data structure

**6. Test Method Refactored (Lines 57-70)**
```python
def test_concat_creates_combined_csv(self):
    """Test that concat.py correctly combines multiple CSV files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup: Create test input files
        self._create_test_csvs(tmpdir)
        script_path = self._get_script_path()

        # Execute: Run the concat script
        self._run_concat_script(tmpdir, script_path)

        # Assert: Verify output contains combined rows
        rows = self._read_output_csv(tmpdir)
        self.assertEqual(rows[0], self.CSV_HEADER)
        self.assertEqual(rows[1:], self.CSV_ROWS_1 + self.CSV_ROWS_2)
```
- Clear three-phase structure: Setup → Execute → Assert
- Self-documenting with inline comments
- Reduced from ~28 lines to ~14 lines
- Much easier to understand test flow

**7. Dead Code Removed**
- Deleted commented-out `setUpClass()` method
- Deleted commented-out `writeDummyCsv()` function
- Removed lines 22-29 of old file

### Results:

| Metric | Before | After |
|--------|--------|-------|
| Test method length | 28 lines | 14 lines |
| Data organization | Scattered in method | Class constants |
| Helper methods | 0 | 4 |
| Comments | None | 4 docstrings + inline comments |
| Dead code | 8 lines | 0 |
| Readability | Medium | **High** |

### Why This is Better:

✅ **Easy to extend** - Add new tests by reusing helper methods  
✅ **Easy to maintain** - Test data in one place, test logic in another  
✅ **Easy to understand** - Clear Setup → Execute → Assert flow  
✅ **Self-documenting** - Method names and docstrings explain intent  
✅ **DRY principle** - No repeated logic or data  
✅ **Follows conventions** - Python and unittest best practices
