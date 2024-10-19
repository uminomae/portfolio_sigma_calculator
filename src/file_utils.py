# portfolio_sigma_calculator/src/file_utils.py
import csv
from typing import List, Tuple
from config import DEBUG_LIST_URLS, PRINT_DEBUG, LOG_DEBUG

def read_urls(file_path: str) -> List[Tuple[str, str]]:
    with open(file_path, 'r') as f:
        return [tuple(line.strip().split(',')) for line in f if line.strip()]

def debug_write_results(DEBUG_LIST_URLS: str, results: List[Tuple[str, str, str, str, str]]):
    if LOG_DEBUG:
        with open(DEBUG_LIST_URLS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Original Name', 'URL', 'Scraped Fund Name', 'Performance'])
            writer.writerows(results)
        # 結果が保存されたことを出力
        print(f"Results saved to {DEBUG_LIST_URLS}")
