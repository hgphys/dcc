"""
SNSの投稿データやブログ記事などのテキストファイルを読み込み、
正規表現を用いてハッシュタグ（#で始まり、空白文字で終わる文字列）を全て抽出するプログラム。
"""
import re

def extract_hashtags(filepath):
    """
    テキストファイルからハッシュタグを抽出して表示する関数
    
    Args:
        filepath (str): テキストファイルのパス
    """
    # ハッシュタグに一致する正規表現パターン
    # #: ハッシュタグ記号
    # \S+: 1文字以上の空白でない文字の連続
    hashtag_pattern = r'\d'

    print(f"--- ハッシュタグ検索開始: {filepath} ---")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # ファイル全体を一つの文字列として読み込む
            content = f.read()
            
            # パターンに一致する部分をすべてリストとして探し出す
            found_hashtags = re.findall(hashtag_pattern, content)
            
            # 一致するハッシュタグが見つかった場合
            if found_hashtags:
                print("投稿から発見したハッシュタグ一覧:")
                for tag in found_hashtags:
                    print(f"- {tag}")
            else:
                print("ハッシュタグは見つかりませんでした。")

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません。パスを確認してください: {filepath}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    print(f"--- ハッシュタグ検索終了 (検索結果: {0} 件) ---")


# メイン処理
if __name__ == '__main__':
    # 読み込むファイルのパスを指定
    file_path = 'data_02/data_02_01.txt'
    
    # 関数を呼び出して処理を実行
    extract_hashtags(file_path)

