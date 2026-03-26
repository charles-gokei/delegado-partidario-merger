#! /usr/bin/env python

import pandas as pd
import glob
import os
from typing import List, Optional


def run(pattern: str = '*.csv', output: str = "delegado_partidario.csv", *, cwd: Optional[str] = None) -> pd.DataFrame:
    # Get all CSV files on current directory
    old_cwd = None
    if cwd:
        old_cwd = os.getcwd()
        os.chdir(cwd)
    try:
        files = list_csv_files(pattern)

        content = [read_csv_file(f) for f in files]

        # Read and concatenates all files into a single dataframe (One single header)
        dataframe = pd.concat(content, ignore_index=True)

        dataframe.to_csv('delegado_partidario.csv', index=False)
    finally:
        if old_cwd:
            os.chdir(old_cwd)


def list_csv_files(pattern: str = "*.csv") -> List[str]:
    files = sorted(glob.glob("*.csv"))
    return files


def read_csv_file(path: str, encoding: str = "latin1", sep=",") -> pd.DataFrame:
    return pd.read_csv(path, encoding='latin1', sep=',')


if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser()
    args.add_argument('--pattern', default='*.csv')
    args.add_argument('--output', default='delegado_partidario.csv')
    parsed = args.parse_args()
    run(parsed.pattern, parsed.output)
