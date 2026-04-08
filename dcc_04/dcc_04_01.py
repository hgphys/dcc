"""
HTMLファイルから商品情報を抽出し、
表形式データとしてExcelファイルに保存するプログラム。
"""

from bs4 import BeautifulSoup
import pandas as pd

def main():
    """
    メイン処理
    """
    input_filepath = 'file path'
    output_filepath_excel = 'data_04/data_04_01.xlsx'
    output_filepath_csv = 'data_04/data_04_01.csv'
    
    try:
        # --- 1. HTMLファイルの読み込み ---
        with open(input_filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # --- 2. HTMLの解析 ---
        # BeautifulSoupのインスタンスを作成し、HTMLを解析
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- 3. データの抽出 ---
        # 抽出したデータを格納するためのリスト
        product_data_list = []
        
        # class="product-item"を持つdivタグをすべて見つける
        product_items = soup.find_all('div', class_='product-item')

        for item in product_items:
            # 各要素から情報を抽出
            data_id = item['data-id']
            product_name = item.find('h2', class_='product-name').text.strip()
            product_meta = item.find('small', class_='product-meta').text.strip()
            price = item.find('span', class_='price').text.strip()
            
            # 抽出したデータを辞書としてリストに追加
            product_data_list.append({
                'data-id': data_id,
                'product-name': product_name,
                'product-meta': product_meta,
                '_____': price #ここを正しく修正
            })
        
        print(f"{len(product_data_list)}件の商品データを抽出しました。")
        
        # --- 4. データフレームの作成 ---
        # データのリストからpandasのDataFrameを作成
        df = pd.DataFrame(product_data_list)
        
        # --- 5. ファイルへの保存 ---
        # Excelファイルとして保存（インデックスは保存しない）
        df.to_excel(output_filepath_excel, index=False)
        print(f"データを '{output_filepath_excel}' に保存しました。")
        
        # CSVファイルとして保存（インデックスは保存しない、文字コードはutf-8-sig）
        df.to_csv(output_filepath_csv, index=False, encoding='utf-8-sig')
        print(f"データを '{output_filepath_csv}' に保存しました。")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()
