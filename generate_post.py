import os
import random
import datetime
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is not set.")
    exit(1)

client = genai.Client(api_key=api_key)

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

# サーバー混雑時の自動リトライ処理（最大3回）
max_retries = 3
for attempt in range(1, max_retries + 1):
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        content = response.text

        os.makedirs("posts", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"記事の生成に成功しました: {filename}")
        break

    except Exception as e:
        print(f"試行 {attempt}/{max_retries} でエラーが発生しました: {e}")
        if attempt < max_retries:
            print("10秒後に再試行します...")
            time.sleep(10)
        else:
            print("再試行上限に達しました。")
            exit(1)
