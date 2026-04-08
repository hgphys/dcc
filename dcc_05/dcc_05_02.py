"""
公開API（郵便番号検索API）を用いて住所データを取得し、
pandasライブラリを用いて整形・ファイル保存するプログラム。
"""

import requests
import pandas as pd
import time
import os

def get_address_from_zipcode(zipcode):
    """
    郵便番号を受け取り、APIを叩いて住所情報を返す関数
    """
    api_url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status() # HTTPエラーがあれば例外を発生させる
        
        data = response.json()
        
        # APIからのステータスが200（成功）で、結果が存在する場合
        if data['status'] == 200 and data['results']:
            # 最初の結果を取得
            result = data['results'][0]
            # 都道府県、市区町村、町域名を結合して返す
            address = f"{result['address1']}{result['address2']}{result['address3']}"
            return address
        else:
            # 住所が見つからなかった場合
            return "見つかりません"

    except requests.exceptions.RequestException as e:
        print(f"エラー: {zipcode} の取得中にHTTPエラーが発生しました: {e}")
        return "取得失敗"
    except (KeyError, TypeError) as e:
        print(f"エラー: {zipcode} の取得中に予期しないデータ形式を受信しました: {e}")
        return "形式エラー"


def main():
    """
    メイン処理
    """
    # 検索対象の郵便番号リスト
    zipcodes = [
        "920-1302"
    ]

    # 保存ファイル名
    output_dir = 'data_05'
    output_filepath_csv = os.path.join(output_dir, 'data_05_02.csv')
    output_filepath_excel = os.path.join(output_dir, 'data_05_02.xlsx')
    
    # フォルダがなければ作成
    os.makedirs(output_dir, exist_ok=True)

    print("--- 郵便番号検索APIから住所情報を取得します ---")
    
    results = []
    for code in zipcodes:
        print(f"{code} を検索中...")
        address = get_address_from_zipcode(code)
        results.append({'郵便番号': code, '住所': address})
        time.sleep(1) # サーバーへの配慮のための1秒待機

    # --- 取得結果をDataFrameに変換して表示 ---
    df = pd.DataFrame(results)
    
    print("\n--- 取得結果一覧 ---")
    print(df)
    
    # --- ファイルへの保存 ---
    # CSVファイルとして保存
    df.to_csv(output_filepath_csv, index=False, encoding="utf-8-sig")
    print(f"\nデータを '{output_filepath_csv}' に保存しました。")
    
    # Excelファイルとして保存
    df.to_excel(output_filepath_excel, index=False)
    print(f"データを '{output_filepath_excel}' に保存しました。")


if __name__ == '__main__':
    main()

