# portfolio_sigma_calculator/src/scraper.py

# HTTP リクエストを行うためのライブラリをインポート
import requests
# HTML 解析のためのライブラリをインポート
from bs4 import BeautifulSoup
# 型ヒントのためのインポート
from typing import Tuple
# 設定ファイルから定数をインポート
from config import HEADERS, START_YEAR, START_MONTH, END_YEAR, END_MONTH
from src.utils import log_debug, print_debug, print_error

import os
import time
from urllib.parse import urljoin
import re
import codecs

def fetch_page_content(session: requests.Session, url: str, headers: dict) -> requests.Response:
    """ ページコンテンツの取得 """
    # ブラウザからアクセスしたようにリクエストヘッダーを付けてURLからデータを取得する
    response = session.get(url, headers=headers)
    # ステータスコードが200以外の場合は例外を発生させる
    response.raise_for_status()
    return response


# HTML からファンド名を抽出する関数
# 戻り値: (ファンド名, 取得方法) の形式のタプル
# soup は引数の名前
# : BeautifulSoup は、引数の型がBeautifulSoupクラス
# -> : この矢印は、関数の戻り値の型
# Tuple[str, str]: これは関数の戻り値の型
# この場合、関数は2つの文字列（str）からなるタプルを返す
# C++の場合
# std::tuple<std::string, std::string> functionName(const BeautifulSoup& soup);
def find_fund_name(soup: BeautifulSoup) -> Tuple[str, str]:
    # デフォルト値を設定
    fund_name = "Fund name not found"
    # すべての h1 タグを取得
    h1_elements = soup.find_all('h1')

    # h1 タグが存在する場合
    if h1_elements:
        # 最初の h1 タグのテキストを取得し、前後の空白を削除
        fund_name = h1_elements[0].text.strip()

    return fund_name

# ダウンロードリンクを処理する
def process_download_link(soup: BeautifulSoup, base_url: str, session: requests.Session, fund_name: str) -> str:
    download_link = soup.find('a', href=lambda x: x and 'Download.do?fnc=' in x)
    if download_link:
        download_page_url = urljoin(base_url, download_link['href'])
        return navigate_and_download(session, download_page_url, fund_name, 
                                     start_year=START_YEAR, start_month=START_MONTH,
                                     end_year=END_YEAR, end_month=END_MONTH)
    # ダウンロードリンクが見つからなかった場合の処理
    return "Download link not found"


# HTML からパフォーマンス値を抽出する関数
def find_performance(soup: BeautifulSoup) -> str:
    # デフォルト値を設定
    performance = "Performance not found"
    # すべての table タグを取得
    tables = soup.find_all('table')

    # 2つ目以降のテーブルが存在する場合
    if len(tables) >= 2:
        # 2つ目のテーブルを対象とする
        target_table = tables[1]
        # テーブル内のすべての行を取得
        rows = target_table.find_all('tr')

        # 2行目以降が存在する場合
        if len(rows) >= 2:
            # 2行目を対象とする
            performance_row = rows[1]
            # 行内のすべてのセルを取得
            cells = performance_row.find_all('td')
            # 2つ目以降のセルが存在する場合
            if len(cells) >= 2:
                # 2つ目のセルのテキストを取得し、前後の空白を削除
                performance = cells[1].text.strip()
        
        # パフォーマンス値が見つからなかった場合
        if performance == "Performance not found":
            log_debug("Performance value not found in the expected location")
        else:
            # パフォーマンス値が見つかった場合
            log_debug(f"Found performance value: {performance}")
        
        # 2つ目のテーブルの構造を出力
        log_debug("\nStructure of the second table:")
        if len(tables) >= 2:
            # 各行の内容を出力
            for i, row in enumerate(tables[1].find_all('tr')):
                log_debug(f"Row {i}: {' | '.join(cell.text.strip() for cell in row.find_all(['th', 'td']))}")
        else:
            log_debug("Second table not found")

    # 取得したパフォーマンス値を返す
    return performance


def scrape_fund_data(url: str) -> Tuple[str, str, str]:
    """ ファンドデータをスクレイプするメイン関数 """
    try:
        log_debug(f"\nAnalyzing URL: {url}")
        print_debug(f"\nAnalyzing URL: {url}")
        # セッションを開始する
        session = requests.Session()
        # ページコンテンツの取得
        response = fetch_page_content(session, url, HEADERS)
        # 取得したHTMLを解析する
        soup = BeautifulSoup(response.text, 'html.parser')
        # ファンド名を取得し、その取得方法も一緒に返す
        fund_name = find_fund_name(soup)
        # パフォーマンス情報を取得する
        performance = find_performance(soup)
        # ダウンロードリンクの取得と処理
        csv_path = process_download_link(soup, url, session, fund_name)
        # ファンド名、取得方法、パフォーマンス、CSVの保存パスを返す
        return fund_name, performance, csv_path
    # リクエスト時にエラーが発生した場合の例外処理
    except requests.RequestException as e:
        print_error(f"Error: {str(e)}")
        return f"Error: {str(e)}", "Error", "Error"

    
    
def navigate_and_download(session: requests.Session, download_page_url: str, fund_name: str, 
                          start_year: int, start_month: int, end_year: int, end_month: int) -> str:
    try:
        
        log_debug(f"Navigating to download page: {download_page_url}")
        
        response = session.get(download_page_url, headers=HEADERS)
        response.raise_for_status()
        download_page_soup = BeautifulSoup(response.text, 'html.parser')

        
        log_debug("Download page HTML content:")
        log_debug(download_page_soup.prettify()[:1000])

        download_form = download_page_soup.find('form', {'name': 'MSFD1101Bean', 'action': lambda x: x and 'DownloadRetYm.do' in x})
        if download_form:
            
            log_debug("Download form found")
            form_url = urljoin(download_page_url, download_form['action'])
            
            form_data = {}
            for input_tag in download_form.find_all(['input', 'select']):
                name = input_tag.get('name')
                if name:
                    if input_tag.name == 'select':
                        selected_option = input_tag.find('option', selected=True)
                        value = selected_option['value'] if selected_option else ''
                    else:
                        value = input_tag.get('value', '')
                    form_data[name] = value

            # Set the start and end year and month
            form_data['selectReturnYearFrom'] = str(start_year)
            form_data['selectReturnMonthFrom'] = str(start_month)
            form_data['selectReturnYearTo'] = str(end_year)
            form_data['selectReturnMonthTo'] = str(end_month)

            download_button = download_form.find('input', type='image', alt='ダウンロード')
            if download_button:
                
                log_debug(f"Download button found: {download_button}")
                button_name = download_button.get('name', 'download')
                form_data[f'{button_name}.x'] = '1'
                form_data[f'{button_name}.y'] = '1'
            else:
                
                log_debug("Warning: Download button not found in the form")

            
            log_debug(f"Form URL: {form_url}")
            log_debug(f"Form data: {form_data}")

            return download_csv(session, form_url, form_data, fund_name, download_page_url)
        else:
            
            log_debug("Download form not found on the download page")
            return "Download form not found on the download page"

    except requests.RequestException as e:
        
        log_debug(f"Error navigating to download page: {str(e)}")
        return f"Error navigating to download page: {str(e)}"

def download_csv(session: requests.Session, url: str, form_data: dict, fund_name: str, referer: str) -> str:
    try:
        headers = HEADERS.copy()
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        headers['Referer'] = referer
        headers['Origin'] = 'https://www.wealthadvisor.co.jp'
        headers['Upgrade-Insecure-Requests'] = '1'

        
        log_debug(f"Sending POST request to: {url}")
        log_debug(f"Headers: {headers}")
        log_debug(f"Form data: {form_data}")

        response = session.post(url, data=form_data, headers=headers, allow_redirects=True)
        response.raise_for_status()

        
        log_debug(f"Response status code: {response.status_code}")
        log_debug(f"Response headers: {response.headers}")
        log_debug(f"Content type: {response.headers.get('Content-Type')}")

        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/csv' in content_type or 'application/csv' in content_type or 'application/octet-stream' in content_type:
            return save_csv_file(response, fund_name)
        elif 'text/html' in content_type:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            log_debug("Response HTML content:")
            log_debug(soup.prettify()[:1000])  # Print first 1000 characters of HTML for debugging
            
            error_message = soup.find('div', class_='error-message')
            if error_message:
                
                log_debug(f"Error message found in response: {error_message.text.strip()}")
                return f"Error: {error_message.text.strip()}"
            
            # Check if there's a download link in the HTML
            download_link = soup.find('a', href=re.compile(r'.*\.csv$'))
            if download_link:
                
                log_debug(f"Found CSV download link: {download_link['href']}")
                csv_url = urljoin(url, download_link['href'])
                return download_csv_file(session, csv_url, fund_name, url)
            
            
            log_debug("No CSV download link found in the HTML response")
            return f"Error: Expected CSV, but got HTML. Check the HTML content for more information."
        else:
            return f"Error: Unexpected content type: {content_type}"

    except requests.RequestException as e:
        
        log_debug(f"Error downloading CSV: {str(e)}")
        return f"Error downloading CSV: {str(e)}"
    except Exception as e:
        
        log_debug(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"

def save_csv_file(response, fund_name: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    download_dir = os.path.join(project_root, 'dl_data')
    os.makedirs(download_dir, exist_ok=True)

    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition and 'filename=' in content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"')
        # Extract the date range from the original filename
        date_range = re.search(r'\d{6}-\d{6}', filename)
        date_range = date_range.group(0) if date_range else ''
    else:
        date_range = f"{int(time.time())}"

    # Clean the fund_name to use in the filename
    clean_fund_name = re.sub(r'[^\w\-_\. ]', '_', fund_name)
    clean_fund_name = clean_fund_name.replace(' ', '_')

    # Create a new filename with the fund name and date range
    filename = f"{clean_fund_name}_{date_range}.csv"
    
    filepath = os.path.join(download_dir, filename)
    
    try:
        # Decode content from Shift-JIS and encode to UTF-8
        content = response.content.decode('shift_jis', errors='replace')
        
        # Save the content with UTF-8 encoding
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        
        log_debug(f"File saved to: {filepath} with UTF-8 encoding")
        
        return filepath
    except Exception as e:
        
        log_debug(f"Error saving file: {str(e)}")
        return f"Error saving file: {str(e)}"





