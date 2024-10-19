# main.py
from config import INPUT_FILE, DEBUG_LIST_URLS, CSV_DIR
from src.file_utils import read_urls, debug_write_results
from src.process_main import process_urls
from src.test.test_diff_comparator import test_main

def main():
    # 入力ファイルからURLデータを読み込む
    url_data = read_urls(INPUT_FILE)
    # URLデータを処理し、結果を取得
    results = process_urls(url_data)
    
    # configのフラグ設定に応じて実行
    debug_write_results(DEBUG_LIST_URLS, results)
    test_main(CSV_DIR)

if __name__ == "__main__":
    main()

# ## TODO
# - refactoring
#   _ scraper.py
# - 機能追加
#   - ポートフォリオのリターン、標準偏差 & 95％区間の下限値の計算
# - グラフ表示
#   - 月次リターンか日次リターンか
#   - データの開始・終了年月
#   - リターン算出の元データの期間