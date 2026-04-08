"""
ファイルから複数の文章を読み込んで一つの文章として扱い、
Bag-of-Words (BoW)の手法でベクトル化し、
文章全体で特徴的な単語（出現回数上位3つ）と、生成されたベクトルを出力するプログラム。
"""

from sklearn.feature_extraction.text import CountVectorizer
from janome.tokenizer import Tokenizer
import numpy as np

def tokenize(text):
    """
    Janomeを使って日本語を分かち書きし、名詞・動詞・形容詞の基本形をリストで返す関数
    """
    t = Tokenizer()
    tokens = []
    for token in t.tokenize(text):
        part_of_speech = token.part_of_speech.split(',')[0]
        if part_of_speech in ['名詞', '動詞', '形容詞']:
            tokens.append(token.base_form)
    return tokens

def get_top_n_words(feature_names, scores, n=3):
    """
    スコア上位の単語を取得するヘルパー関数
    """
    # スコアを降順にソートしたインデックスを取得
    sorted_indices = np.argsort(scores)[::-1]
    # 上位n個の単語とスコアを返す
    top_features = [(feature_names[i], scores[i]) for i in sorted_indices[:n]]
    return top_features

def main():
    """
    メイン処理
    """
    input_filepath = 'file path'

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            # 1行を1文書としてリストに読み込む
            documents = [line.strip() for line in f.readlines()]
        
        # 全てのレビューを一つの大きな文章に結合
        full_text = " ".join(documents)
        
        # これから分析する文章は一つだけなのでリストに入れる
        corpus = [full_text]

        print(f"--- 分析対象の文章 ---\n{full_text}\n")

        # --- Bag-of-Words (BoW) ---
        print("--- Bag-of-Words (BoW)による分析 ---")
        # CountVectorizer: 単語の出現回数をカウント
        bow_vectorizer = CountVectorizer(tokenizer=tokenize)
        bow_matrix = bow_vectorizer.fit_transform(corpus)
        bow_feature_names = np.array(bow_vectorizer.get_feature_names_out())
        
        # corpusは要素が1つだけなので、[0]で最初の文章の結果を取得
        scores = bow_matrix.toarray()[0] 
        
        # BoWベクトルと語彙の表示を追加
        print("\n[BoWによるベクトル化の結果]")
        print(f"語彙リスト (Vocabulary): {bow_feature_names.tolist()}")
        print(f"BoWベクトル (各単語の出現回数): {scores.tolist()}")

        # 文章全体での上位3単語を出力
        print("\n[頻出単語 Top 3]")
        top_words = get_top_n_words(bow_feature_names, scores)
        print(f"  -> BoW上位: {[(word, f'{score:.0f}') for word, score in top_words]}")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()

