# CSV Concatenator

A Python utility to concatenate multiple CSV files into a single consolidated dataset.

## Features

- Combines multiple CSV files with consistent headers
- Maintains data integrity during concatenation
- Deterministic file ordering (alphabetical)
- Configurable CSV format (delimiter, encoding)
- Command-line interface with flexible options

## Requirements

- Python 3.7+
- pandas
- (See `requirements.txt` for details)

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd delegado_partidario
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

**Basic usage** - concatenate all CSV files in current directory:
```bash
python concat.py
```

This will create `delegado_partidario.csv` by combining all CSV files in the current directory.

**With custom pattern** - concatenate specific CSV files:
```bash
python concat.py --pattern "delegado_partidario_*.csv"
```

**With custom output file**:
```bash
python concat.py --output combined.csv
```

**Combined options**:
```bash
python concat.py --pattern "data_*.csv" --output final_output.csv
```

### Python API

Import and use the concatenation function in your own code:

```python
from concat import concatenate_csv_files

# Basic usage
result = concatenate_csv_files()

# With custom parameters
result = concatenate_csv_files(
    pattern="delegado_partidario_*.csv",
    output="combined.csv",
    encoding="latin1",
    sep=","
)

# With custom working directory
result = concatenate_csv_files(
    pattern="*.csv",
    output="result.csv",
    cwd="/path/to/data"
)
```

## Testing

### Run Tests

Execute the test suite:
```bash
python -m unittest test_concat.py
```

Or with verbose output:
```bash
python -m unittest test_concat.py -v
```

### What the Tests Cover

The test suite (`test_concat.py`) verifies:
- CSV files are correctly read and parsed
- Headers are properly combined
- Data rows are concatenated in the correct order (alphabetical by filename)
- Output file is created successfully
- Encoding is handled correctly

### Run a Specific Test

```bash
python -m unittest test_concat.ConcatScriptTest.test_concat_creates_combined_csv
```

## Examples

### Example 1: Concatenate Party Delegate Files

If you have files like:
- `delegado_partidario_PT.csv`
- `delegado_partidario_PSL.csv`
- `delegado_partidario_PSDB.csv`

Run:
```bash
python concat.py --pattern "delegado_partidario_*.csv" --output delegado_partidario.csv
```

Result: All party delegate files combined into a single `delegado_partidario.csv` file.

### Example 2: Process Files in a Specific Directory

```bash
python concat.py --pattern "*.csv" --output /output/combined.csv
```

(Note: The script changes to the specified working directory before processing)

## CSV Format

**Expected format:**
- Delimiter: `,` (comma) - standard CSV format
- Encoding: `latin1` (ISO-8859-1)
- First row: Column headers
- Consistent structure across all files

**Example input files:**

`file1.csv`:
```
col1,col2,col3
John,25,Engineer
Jane,30,Manager
```

`file2.csv`:
```
col1,col2,col3
Bob,28,Designer
Alice,32,Analyst
```

**Output** (`delegado_partidario.csv`):
```
col1,col2,col3
John,25,Engineer
Jane,30,Manager
Bob,28,Designer
Alice,32,Analyst
```

## Troubleshooting

### No CSV files found
**Error:** `ValueError: No CSV files found matching pattern: ...`

**Solution:** Make sure:
- You're in the correct directory
- CSV files exist matching your pattern
- Pattern syntax is correct (e.g., `*.csv`, `data_*.csv`)

### Encoding issues
**Error:** `UnicodeDecodeError`

**Solution:** The default encoding is `latin1`. If your files use a different encoding, modify the script or specify when calling the function.

### Incorrect delimiter
**Error:** Columns are not separated correctly in output

**Solution:** The script expects comma-delimited CSV files. If you have semicolon-delimited files, you'll need to convert them first.

## Development

### Code Structure

- `concat.py` - Main script with concatenation logic
- `test_concat.py` - Unit tests for the concatenation functionality
- `requirements.txt` - Python dependencies

### Running Tests During Development

```bash
# Run tests and watch for changes
python -m unittest test_concat.py --verbose
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here if applicable]
