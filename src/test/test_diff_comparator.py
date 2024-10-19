# src/test/test_diff_comparator.py
from src.utils import log_debug, print_debug, print_error
import pandas as pd
from pathlib import Path
import os
from config import DEBUG_LIST_URLS, PRINT_DEBUG, LOG_DEBUG, RUN_TEST

def compare_csv_files(file1, file2):
    try:
        if not Path(file1).is_file() or not Path(file2).is_file():
            print_error(f"One of the files does not exist: {file1}, {file2}")
            return

        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # 差分を取る
        if df1.equals(df2):
            print_debug("The CSV files are identical.")
        else:
            # 差分がある場合、それを出力
            differences = pd.concat([df1, df2]).drop_duplicates(keep=False)
            print_error(f"Differences found between {file1} and {file2}:\n{differences}")

    except Exception as e:
        print_error(f"Error while comparing files: {str(e)}")

def test_main(csv_dir: str):
    if RUN_TEST:
        file_path = os.path.join(csv_dir, 'combined_returns.csv')
        compare_csv_files('src/test/files_to_compare/combined_returns.csv', file_path)
