# portfolio_sigma_calculator/main.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple
from config import INPUT_FILE, OUTPUT_FILE, CSV_DIR
from src.file_utils import read_urls, debug_write_results
from src.scraper import scrape_fund_data
import matplotlib.pyplot as plt
from src.csv_integration import generate_heatmap
from src.utils import log_debug, print_debug, print_error

def set_japanese_font() -> None:
    """日本語フォントの設定を行う"""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 
                                       'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


def process_fund_data(original_name: str, url: str) -> Tuple[str, str, str]:
    """ファンドデータを取得し、デバッグ情報を出力した後、ファンドデータを返す"""
    # 各URLに対して、ファンドデータを取得
    fund_name, performance, csv_path = scrape_fund_data(url)
    # デバッグ情報の出力
    log_debug(f"Processed: {original_name}")
    log_debug(f"  Fund Name: {fund_name}")
    log_debug(f"  Performance: {performance}")
    log_debug(f"  CSV File: {csv_path}\n")
    # 取得したデータをリターン
    return fund_name, performance, csv_path


def process_csv(csv_path: str, fund_name: str) -> pd.DataFrame:
    """CSVファイルを読み込み、日付をインデックスに設定したDataFrameを返す"""
    # CSVファイルが存在するか確認
    if os.path.exists(csv_path):
        # CSVファイルを読み込み、DataFrameに変換
        df = pd.read_csv(csv_path)
        # 日付列を「年-月」形式の日付型に変換
        df['日付'] = pd.to_datetime(df['日付'], format='%Y%m')
        # 日付列をインデックスとして設定
        df = df.set_index('日付')
        # DataFrameのカラム名をファンド名に設定
        df.columns = [fund_name]
        return df
    else:
        print_error(f"CSV file not found: {csv_path}")
        return None


def delete_csv_files(csv_files: List[str]) -> None:
    """CSVファイルをリストから削除する"""
    for csv_file in csv_files:
        try:
            os.remove(csv_file)
        except OSError as e:
            print_error(f"Error deleting file {csv_file}: {e}")
    
    log_debug(f"CSV file deleted")


def process_urls(url_data: List[Tuple[str, str]]) -> List[Tuple[str, str, str, str, str]]:
    """URLリストを処理し、ファンド情報とCSVファイルをまとめる"""
    # 日本語フォントの設定を行う
    set_japanese_font()

    # 処理結果を格納するリスト
    results = []
    # ヒートマップ生成のために、DataFrameを格納するリスト
    dataframes = []
    # 削除するCSVファイルのパスを格納するリスト
    csv_files_to_delete = []

    # URLデータのリストをループ処理
    for original_name, url in url_data:
        # サブ関数でファンドデータを処理し、その結果を受け取る
        fund_name, performance, csv_path = process_fund_data(original_name, url)
        # 取得したデータをresultsリストに追加
        results.append((original_name, url, fund_name, performance, csv_path))
        # CSVファイルの処理を行い、DataFrameをリストに追加
        df = process_csv(csv_path, fund_name)
        if df is not None:
            dataframes.append(df)
            # 後で削除するために、CSVファイルのパスをリストに追加
            csv_files_to_delete.append(csv_path)

    # ヒートマップを生成し、CSVディレクトリに保存
    generate_heatmap(dataframes, CSV_DIR)
    # 処理が終わった後にファンドごとに出力したCSVファイルを削除する
    delete_csv_files(csv_files_to_delete)

    return results
