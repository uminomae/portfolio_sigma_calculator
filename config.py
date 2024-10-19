# portfolio_sigma_calculator/config.py


# ---------------------------------
# 設定について
# ---------------------------------

# - 開始と終了年月を設定してください。
# - 他の項目は必要に応じて変更してください。

# ---------------------------------
# 取得する月次リターンの期間
# ---------------------------------

# 開始年月設定
# START_YEAR = 2021
# START_MONTH = 10
START_YEAR = 2024
START_MONTH = 1

# 個人用
# START_YEAR = 2021
# START_MONTH = 6

# 終了年月設定
END_YEAR = 2024
END_MONTH = 9


# ---------------------------------------------------------------------------------------------------

# ---------------------------------
# ポートフォリオ計算用の定数
# ---------------------------------

RISK_FREE_RATE = 0.02  # 年間2%のリスクフリーレートを仮定

# ---------------------------------
# 入出力先
# ---------------------------------
# 計算に必要な情報（wealthadvisor.co.jpのURLなど）を記述するファイル
INPUT_FILE = 'input.csv'
# INPUT_FILE = 'input2.csv'

# 処理した内容の保存先ディレクトリ　※相関行列の画像など
CSV_DIR = 'reports'

# 処理内容を確認するためのファイル
OUTPUT_FILE = 'output.csv'


# ---------------------------------------------------------------------------------------------------

# ---------------------------------
# デバッグなど
# ---------------------------------

# アプリケーション名
APP_NAME = "Portfolio Sigma Calculator"

# Test
RUN_TEST = True

# Debug mode flag
PRINT_DEBUG = True
LOG_DEBUG = False
# LOG_DEBUG = True

# HTTP request headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

