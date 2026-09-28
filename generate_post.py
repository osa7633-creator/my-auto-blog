import os
import glob
import random
import time
from datetime import datetime
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is not set.")
    exit(1)

client = genai.Client(api_key=api_key)

# 1. 過去記事の取得（重複防止）
existing_files = glob.glob("posts/*.md")
past_titles = [os.path.basename(f).replace(".md", "") for f in existing_files]
past_titles_str = "\n".join(past_titles[-20:]) if past_titles else "なし"

# 2. テーマを大幅に多角化（車系案件の審査対策を強化）
themes = [
    # 車・買取り・処分（A8審査対策）
    "中古車を高く売るための相見積もりのコツとタイミング",
    "動かない車・年式が古い車を処分・買取してもらう方法",
    "車検を通すか買い替えるか？損しない判断基準",
    "一括査定サービスのメリット・デメリットと電話ラッシュ対策",
    "車の売却時に必要な書類と手続きの流れ解説",
    
    # ガジェット・デスク環境
    "リモートワークの生産性を劇的に上げるおすすめガジェット5選",
    "デュアルモニター環境の構築方法と作業効率の変化",
    "疲れないオフィスチェア・昇降デスクの選び方",
    
    # AI・プログラミング・自動化
    "ChatGPT・Geminiを日常業務で使い倒すプロンプト例",
    "Pythonを使った日常の単純作業自動化アイデア",
    "個人開発者が知っておくべき無料インフラ・ホスティングサービス",
    
    # 資産形成・節約・キャリア
    "固定費削減！真っ先に見直すべきサブスクと通信費",
    "副業ブログで最初の1万円を稼ぐためのステップ",
    "時間を作るための『やらないことリスト』の作成手順"
]

selected_theme = random.choice(themes)

prompt = f"""
あなたはプロのWebライターです。
以下の【指定テーマ】について、読者の疑問や悩みを解決する高品質なブログ記事を1本作成してください。

【指定テーマ】: {selected_theme}

【厳守事項・重複禁止】
以下の過去記事タイトルとは内容や切り口が「絶対に被らない」ように執筆してください。
--- 過去に投稿済みの記事一覧 ---
{past_titles_str}
--------------------------------

【文章構成】
- タイトル（# タイトル）
- 導入（読者の悩みに共感し、記事で得られるメリットを提示）
- 本文（H2, H3見出しを使い、具体的な手順や理由を分かりやすく解説）
- まとめ

Markdown形式で出力し、コードブロック（```markdown 等）で囲まずに直接出力してください。
"""

max_retries = 3
for attempt in range(1, max_retries + 1):
    try:
        print(f"記事生成中... テーマ: {selected_theme}")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        content = response.text.strip()
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        now = datetime.now()
        filename = f"posts/{now.strftime('%Y-%m-%d-%H%M%S')}.md"
        os.makedirs("posts", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Successfully generated: {filename}")
        break

    except Exception as e:
        print(f"一時的エラー (試行 {attempt}/{max_retries}): {e}")
        if attempt < max_retries:
            time.sleep(10)
        else:
            print("混雑のため本日の生成をスキップします。")
            exit(0)
