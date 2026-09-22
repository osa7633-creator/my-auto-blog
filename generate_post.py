import os
import re
import random
import time
from datetime import datetime
from google import genai

TOPICS = [
    "中古車を高値で売るコツとおすすめの一括査定サービス",
    "動かない車や古い事故車でも高く買い取ってもらう方法",
    "【2026年最新】軽自動車の買取相場と査定額をアップさせるコツ",
    "走行距離10万キロ超えでも諦めない！愛車を高く売る完全攻略ガイド",
    "車の買い替えで10万円以上得する最適なタイミング5選"
]

MODEL_NAME = "gemini-3.6-flash"

def clean_markdown(text):
    text = re.sub(r"^```markdown\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
    return text.strip()

def generate_article():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("環境変数 GEMINI_API_KEY が設定されていません。")

    client = genai.Client(api_key=api_key)
    topic = random.choice(TOPICS)
    print(f"--- 選択テーマ: {topic} ---")

    prompt = f"""
あなたは自動車買取・査定のプロブロガーです。
以下のテーマについて、読者にとって非常に役立つブログ記事（Markdown形式）を執筆してください。

テーマ: {topic}

制約事項:
1. 記事の1行目は必ず `# タイトル` の形式（H1タグ）にしてください。
2. 構成: はじめに、車を高く売るポイント、おすすめの対策、まとめ。
3. 読者が納得して一括査定などのサービスを使いたくなるような、親しみやすく丁寧な解説を行ってください。
4. マークダウン文章のみを出力してください（``` などのコード囲みは含めないでください）。
"""

    max_retries = 3
    article_content = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Gemini API呼び出し中... ({MODEL_NAME} / 試行 {attempt}/{max_retries})")
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            if response and response.text:
                article_content = clean_markdown(response.text)
                print("記事の生成に成功しました！")
                break

        except Exception as e:
            err_msg = str(e)
            # 429 (1日上限到達) の場合はリトライせず即時終了する
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                print(f"【通知】{MODEL_NAME} の1日あたりの無料利用上限（20回）に達しました。本日の自動生成をスキップします。")
                return

            print(f"一時的なエラー (試行 {attempt}/{max_retries}): {err_msg}")
            if attempt < max_retries:
                time.sleep(15 * attempt)

    if not article_content:
        raise RuntimeError("記事の取得に失敗しました。")

    os.makedirs("posts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"posts/post_{timestamp}.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article_content)

    print(f"保存完了: {filepath}")

if __name__ == "__main__":
    generate_article()
