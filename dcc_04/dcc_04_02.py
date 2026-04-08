"""
金沢学院大学の教員一覧ページをスクレイピングし、
教員の氏名と専門分野を抽出してファイルに保存するプログラム。
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
import os

def main():
    """
    メイン処理
    """
    # スクレイピング対象のURL
    target_url = "target url"
    
    # --- 1. robots.txtの確認 ---
    # robots.txtのURLを作成
    robots_url = urljoin(target_url, '/robots.txt')
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    
    # スクレイピングが許可されているかを確認
    user_agent = '*'
    if not rp.can_fetch(user_agent, target_url):
        print(f"'{robots_url}' により、'{target_url}' へのアクセスは許可されていません。")
        return

    print(f"'{target_url}' へのアクセスは許可されています。スクレイピングを開始します。")

    try:
        # --- 2. WebページのHTMLを取得 ---
        # サーバーに配慮して1秒待機
        time.sleep(1) 
        response = requests.get(target_url)
        # HTTPステータスコードが200以外の場合はエラーとして終了
        response.raise_for_status() 
        html = response.text

        # --- 3. HTMLの解析とデータ抽出 ---
        soup = BeautifulSoup(html, "html.parser")
        
        data = []
        for item in soup.find_all("li", class_="archiveTeacherbox__item"):
            name = item.find("span", class_="archiveTeacherbox__name").text.strip()
            specialty = item.find("span", class_="archiveTeacherbox__senmonsp").text.strip()
            data.append([name, specialty])
        
        print(f"{len(data)}件のデータを抽出しました。")

        # --- 4. データの整形とファイル保存 ---
        if not data:
            print("抽出できるデータがありませんでした。")
            return

        df = pd.DataFrame(data, columns=["氏名", "専門分野"])
        df = df.drop_duplicates()
        print(f"重複削除後、{len(df)}件のデータになりました。")

        # 保存先フォルダの確認・作成
        output_dir = 'data_04'
        os.makedirs(output_dir, exist_ok=True)
        
        output_filepath_csv = os.path.join(output_dir, 'data_04_02.csv')
        output_filepath_excel = os.path.join(output_dir, 'data_04_02.xlsx')

        # CSVファイルに保存
        df.to_csv(output_filepath_csv, index=False, encoding="utf-8-sig")
        print(f"データを '{output_filepath_csv}' に保存しました。")
        
        # Excelファイルに保存
        df.to_excel(output_filepath_excel, index=False)
        print(f"データを '{output_filepath_excel}' に保存しました。")

    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストエラー: {e}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()
