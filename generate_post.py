import os
import random
import datetime
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is not set.")
    exit(1)

genai.configure(api_key=api_key)

# 動作するモデル名に指定を変更
model = genai.GenerativeModel('gemini-1.5-flash')

THEMES = [
    "動かない車・年式が古い車を処分・買取してもらう方法",
    "カーリースのメリット・デメリットを徹底解説",
    "新車購入とカーリースはどちらがお得か比較",
    "車検費用を安く抑えるコツと注意点",
    "中古車を購入する際に見るべき重要なポイント",
    "マイカーローンとカーリースの月々の支払額を比較",
    "失敗しない中古車の選び方とチェックリスト"
]

theme = random.choice(THEMES)
today_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"posts/post_{today_str}.md"

prompt = f"""
あなたは自動車の専門ライターです。
以下のテーマについて、読者にとって役立つ検索SEOに強いブログ記事をMarkdown形式で執筆してください。

テーマ: {theme}

【構成の指定】
1. タイトルは「# タイトル」の形式で一番上に書いてください。
2. 見出しには「## 」「### 」を使用してください。
3. 文章の途中に適宜「[AFFILIATE_LINK_1]」というタグを1個挟んでください。

記事本文のみを出力してください。
"""

print(f"記事生成中... テーマ: {theme}")

try:
    response = model.generate_content(prompt)
    content = response.text

    os.makedirs("posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"記事の生成に成功しました: {filename}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit(1)
