# main.py
from config import INPUT_FILE, OUTPUT_FILE, CSV_DIR
from src.file_utils import read_urls, debug_write_results
from src.file_utils import read_urls
from src.process_main import process_urls
from src.test.test_diff_comparator import test_main

def main():
    # 入力ファイルからURLデータを読み込む
    url_data = read_urls(INPUT_FILE)
    # URLデータを処理し、結果を取得
    results = process_urls(url_data)
    
    # configのフラグ設定に応じて実行
    debug_write_results(OUTPUT_FILE, results)
    test_main(CSV_DIR)

if __name__ == "__main__":
    main()

# ## TODO
# - refactoring
#   _ scraper.py
# - 機能追加
#   - ポートフォリオのリターン、標準偏差 & 95％区間の下限値の計算
