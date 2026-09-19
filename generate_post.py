import os
import random
from datetime import datetime
from google import genai

# 車関連の自動生成テーマリスト
TOPICS = [
    "中古車を高値で売るコツとおすすめの一括査定サービス",
    "車の買い替えで損しないための最適なタイミング",
    "ディーラー下取りと車買取専門店の買取額の違いとメリット",
    "動かない車や古い事故車でも高く買い取ってもらう方法",
    "車査定でのしつこい営業電話を回避してスマートに売る方法",
    "軽自動車の買取相場と査定額をアップさせるチェックポイント",
    "走行距離10万キロ超えの車でも高く売るための注意点",
    "愛車を手放す時の必要書類とスムーズな手続きの流れ",
]

def generate_article():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。")

    client = genai.Client(api_key=api_key)

    # ランダムにテーマを選択
    topic = random.choice(TOPICS)
    print(f"今回の選択テーマ: {topic}")

    prompt = f"""
あなたは車買取・査定に詳しいプロのブロガーです。
以下のテーマについて、読者の悩みを解決するSEOに強いブログ記事を日本語で作成してください。

【テーマ】: {topic}

【構成の指定】:
- H1タイトル（魅力的でクリックしたくなるタイトル）
- 導入文（読者の共感を呼び、記事を読むメリットを伝える）
- H2見出し 3〜4つ（読みやすい解説、具体的なアドバイス）
- まとめ（読者の背中を押す文面、査定申込みを促す文言）

※アフィリエイト広告を入れるためのタグ「{{AFFILIATE_1}}」を、導入文の直後とまとめの直前に1つずつ配置してください。
※出力はMarkdown形式のみ（```markdown などの囲み枠は不要）にしてください。
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    # 保存用ファイル名の作成
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("posts", exist_ok=True)
    filename = f"posts/post_{now}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"記事を生成しました: {filename}")

if __name__ == "__main__":
    generate_article()