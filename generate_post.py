import os
import sys
from google import genai

# Gemini APIキーの設定（取得したキーを直接指定するか環境変数から読み込み）
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_article(topic):
    prompt = f"""
あなたは車に関するブログの専門ライターです。
以下のテーマについて、読者にとって役立つ詳細なブログ記事をMarkdown形式で作成してください。

テーマ: {topic}

【執筆ルール】
1. 1行目には記事タイトル（H1見出し `# タイトル`）を書くこと。
2. 見出し（H2 `##`, H3 `###`）を適切に使って構成すること。
3. 記事の中盤および最後に、必ずアフィリエイトリンクのプレースホルダー `{{{{AFFILIATE_1}}}}` または `{{{{AFFILIATE_2}}}}` を自然な形で配置すること。
4. Markdown文章のみを出力し、コードブロックの囲み（```markdown など）や余計な挨拶文は一切出力しないこと。
"""

    print(f"🤖 「{topic}」に関する記事をAIが生成中...")
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    content = response.text.strip()
    
    # 1行目のタイトルからファイル名を作成
    lines = content.splitlines()
    first_line = lines[0].replace("#", "").strip() if lines else "new_post"
    
    # 記号を除去してファイル名に使える文字列に変換
    clean_filename = "".join([c for c in first_line if c.isalnum() or c in (' ', '_', '-')]).rstrip()
    if not clean_filename:
        clean_filename = "generated_post"
        
    output_path = f"posts/{clean_filename}.md"
    os.makedirs("posts", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ 記事の生成に成功しました: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("生成したい記事のテーマを入力してください: ")
        
    generate_article(topic)