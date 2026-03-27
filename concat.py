#!/usr/bin/env python
"""Concatenate multiple CSV files into a single dataset."""

import os
import glob
from contextlib import contextmanager
from typing import List, Optional

import pandas as pd
import argparse


@contextmanager
def change_directory(path: Optional[str]):
    """Context manager for safely changing working directory."""
    old_cwd = None
    try:
        if path:
            old_cwd = os.getcwd()
            os.chdir(path)
        yield
    finally:
        if old_cwd:
            os.chdir(old_cwd)


def concatenate_csv_files(
    pattern: str = "*.csv",
    output: str = "delegado_partidario.csv",
    encoding: str = "latin1",
    sep: str = ";",
    cwd: Optional[str] = None
) -> pd.DataFrame:
    """
    Concatenate all CSV files matching a pattern into a single file.
    
    Args:
        pattern: Glob pattern to find CSV files (default: "*.csv")
        output: Output filename (default: "delegado_partidario.csv")
        encoding: File encoding (default: "latin1")
        sep: CSV delimiter (default: ";")
        cwd: Working directory (default: current directory)
    
    Returns:
        The concatenated DataFrame
    """
    with change_directory(cwd):
        files = list_csv_files(pattern)
        
        if not files:
            raise ValueError(f"No CSV files found matching pattern: {pattern}")
        
        dataframes = [
            read_csv_file(f, encoding=encoding, sep=sep)
            for f in files
        ]
        
        result = pd.concat(dataframes, ignore_index=True)
        result.to_csv(output, index=False, encoding=encoding, sep=sep)
        
        return result


def list_csv_files(pattern: str = "*.csv") -> List[str]:
    """List all CSV files matching the pattern, sorted alphabetically."""
    return sorted(glob.glob(pattern))


def read_csv_file(
    path: str,
    encoding: str = "latin1",
    sep: str = ";"
) -> pd.DataFrame:
    """Read a single CSV file into a DataFrame."""
    return pd.read_csv(path, encoding=encoding, sep=sep)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate CSV files into a single dataset"
    )
    parser.add_argument(
        "--pattern",
        default="*.csv",
        help="Glob pattern to find CSV files (default: *.csv)"
    )
    parser.add_argument(
        "--output",
        default="delegado_partidario.csv",
        help="Output filename (default: delegado_partidario.csv)"
    )
    parser.add_argument(
        "--sep",
        default=";",
        help="CSV delimiter (default: ;)"
    )
    parser.add_argument(
        "--encoding",
        default="latin1",
        help="File encoding (default: latin1)"
    )
    
    args = parser.parse_args()
    concatenate_csv_files(args.pattern, args.output, args.encoding, args.sep)
