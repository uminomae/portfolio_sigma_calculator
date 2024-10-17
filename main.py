# portfolio_sigma_calculator/main.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
from config import INPUT_FILE, OUTPUT_FILE, DEBUG, CSV_DIR
from src.file_utils import read_urls, write_results
from src.scraper import scrape_fund_data
import matplotlib.pyplot as plt
import matplotlib as mpl
import japanize_matplotlib
from src.csv_integration import generate_heatmap

def process_urls(url_data: List[Tuple[str, str]]) -> List[Tuple[str, str, str, str, str]]:
    # 日本語フォントの設定
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

    results = []
    dataframes = []

    for original_name, url in url_data:
        fund_name, method, performance, csv_path = scrape_fund_data(url)
        
        results.append((original_name, url, fund_name, method, performance, csv_path))

        if DEBUG:
            print(f"Processed: {original_name}")
            print(f"  Fund Name: {fund_name} (Method: {method})")
            print(f"  Performance: {performance}")
            print(f"  CSV File: {csv_path}\n")
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df['日付'] = pd.to_datetime(df['日付'], format='%Y%m')
            df = df.set_index('日付')
            df.columns = [fund_name]
            dataframes.append(df)

    generate_heatmap(dataframes, CSV_DIR)  # ヒートマップ生成関数を呼び出し

    if DEBUG:
        print("Correlation matrix created and saved as 'correlation_heatmap.png'")
        print("Combined returns data saved as 'combined_returns.csv'")

    

    return results

def main():
    url_data = read_urls(INPUT_FILE)
    results = process_urls(url_data)
    write_results(OUTPUT_FILE, results)
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()