"""
ファイルから1つの文章を読み込み、形態素解析を実行して、
各単語（形態素）の情報を一覧で出力するプログラム。
"""

from janome.tokenizer import Tokenizer

def main():
    """
    メイン処理
    """
    input_filepath = 'file path'
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            # ファイルから文章を一行読み込む
            text = f.read().strip()

        # Tokenizerのインスタンスを作成
        t = Tokenizer()

        print(f"--- 元の文章 ---\n{text}\n")
        print("--- 形態素解析の結果 ---")
        # ヘッダーを簡潔な表示に変更
        print("表層形\t品詞\t基本形")
        print("-" * 20)

        # 形態素解析を実行し、結果を一つずつ表示
        for token in t.tokenize(text):
            # tokenオブジェクトから品詞情報を取得し、カンマで分割して最初の要素（主要な品詞）のみを取り出す
            part_of_speech = token.part_of_speech.split(',')[0]
            
            # 各情報をタブ区切りで出力
            print(f"{token.surface}\t{part_of_speech}\t{token.base_form}")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()

