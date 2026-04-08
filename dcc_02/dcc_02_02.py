"""
商品リストを読み込み、データ整形（表記揺れの統一）を行う。
整形によって変更があった行について、変更前と変更後を比較表示を行い、
最後に、全ての行を整形した後の完全なリストを新しいファイルに保存するプログラム。
"""

import unicodedata

def clean_text(text):
    """
    文字列の全角英数字・記号を半角に正規化し、前後の空白を削除する関数
    """
    # NFKC（Normalization Form KC）形式で正規化し、全角文字を半角に変換
    normalized_text = unicodedata.normalize('NFKC', text)
    # 文字列の前後の空白（スペース、タブ、改行など）を削除
    stripped_text = normalized_text.strip()
    return stripped_text

def main():
    """
    メイン処理
    """
    input_filepath = 'data_02/data_02_02.txt'
    output_filepath = 'data_02/data_02_02_cleaned.txt'
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print("--- 整形によって変更された行 ---")
        
        all_cleaned_lines = []
        changed_count = 0

        for original_line in lines:
            # 元の行から末尾の改行コードを削除して比較用に保持
            original_line_stripped = original_line.strip()
            
            # データを整形
            cleaned_line = clean_text(original_line)
            
            # 整形後のデータをリストに追加
            all_cleaned_lines.append(cleaned_line)

            # 整形前と整形後で変化があったかチェック
            if original_line_stripped != cleaned_line:
                print(f"変更前: {original_line_stripped}")
                print(f"変更後: {cleaned_line}")
                print("-" * 20) # 区切り線
                changed_count += 1
        
        if changed_count == 0:
            print("表記揺れのある行は見つかりませんでした。")
        else:
            print(f"表記揺れ修正件数: {0}件")

        # 整形後の全データを新しいファイルに保存
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for line in all_cleaned_lines:
                f.write(line + '\n')
        
        print(f"\n整形後のデータを以下に保存しました。")
        print(f"保存先: '{output_filepath}' ")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()

