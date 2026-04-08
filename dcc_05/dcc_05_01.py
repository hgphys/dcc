"""
e-Statからダウンロードした都道府県別の人口データから、
pandasライブラリを用いて石川県の2024年の男女別人口を抽出するプログラム。

■事前準備:
1. e-Statの「人口推計」ページにアクセス。
URL: https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200524&tstat=000000090001&cycle=7&year=20240&month=0&tclass1=000001011679&result_back=1&tclass2val=0
2. 表番号5「都道府県、男女別人口－総人口、日本人人口（各年10月1日現在）」のExcelファイルをダウンロードしてください。
3. ダウンロードしたファイルを 'data_05' フォルダ内に保存してください。
"""

import pandas as pd
import os

def main():
    """
    メイン処理
    """
    input_filepath = os.path.join('data_05', 'file name')

    try:
        # --- 1. Excelファイルの読み込み ---
        # e-StatのExcelファイルは、ファイルの先頭に説明などの不要な行が含まれている。
        # データの本体（ヘッダー行）が始まる7行目までを `skiprows=6` で読み飛ばす。
        df = pd.read_excel(input_filepath, skiprows=6)
        
        # --- 2. データの整形と抽出 ---
        # 列名に含まれる可能性のある空白を削除
        df.columns = df.columns.str.strip()
        
        # '地域' 列のデータに含まれる空白を削除
        df['地域'] = df['地域'].str.strip()

        # 石川県の総人口データのみを抽出
        ishikawa_df = df[(df['地域'] == '石川県') & (df['人口区分'] == '総人口')].copy()

        # 2024年の男性人口を取得
        male_pop_thousand = ishikawa_df.loc[ishikawa_df['性別'] == '男', '2024年'].iloc[0]
        
        # 2024年の女性人口を取得
        female_pop_thousand = ishikawa_df.loc[ishikawa_df['性別'] == '女', '2024年'].iloc[0]

        # 単位は「千人」なので1000倍する
        male_pop = male_pop_thousand * 1000
        female_pop = female_pop_thousand * 1000

        # --- 3. 結果の表示 ---
        print("--- 石川県の2024年10月1日時点の推計人口 ---")
        print(f"男性: {male_pop:,.0f} 人")
        print(f"女性: {female_pop:,.0f} 人")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
        print("説明文に従ってe-StatからExcelファイルをダウンロードし、指定の場所に配置したか確認してください。")
    except IndexError:
        print("エラー: 石川県のデータが見つかりませんでした。")
        print("ダウンロードしたファイルが正しいか、またはファイルの内容を確認してください。")
    except KeyError as e:
        print(f"エラー: {e} という列が見つかりません。")
        print("ダウンロードしたファイルの年が正しいか、またはヘッダー行の位置('skiprows')が正しいか確認してください。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()

