import os
import time
import requests
import urllib.parse

# 設定項目
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5"
REPO_PATH = "./"
POSTS_DIR = os.path.join(REPO_PATH, "posts")

SEED_KEYWORDS = ["おすすめ", "選び方", "コスパ", "レビュー"]

def fetch_suggest_keywords(seed):
    encoded_seed = urllib.parse.quote(seed)
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=ja&q={encoded_seed}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()[1]
    except Exception as e:
        print(f"[エラー] キーワード取得失敗 ({seed}): {e}")
        return []

PROMPT_TEMPLATE = """
以下のキーワードに関するWeb比較・解説記事をMarkdown形式で作成してください。

キーワード: {keyword}

【構成要件】
1. 悩みに寄り添う導入
2. おすすめアイテム3選（プレースホルダーとして [AFFILIATE_LINK_1], [AFFILIATE_LINK_2], [AFFILIATE_LINK_3] を含める）
3. 選ぶ際の注意点
4. まとめ

SEOに最適化し、2000文字程度の日本語で出力してください。
"""

def generate_article(keyword):
    payload = {
        "model": MODEL_NAME,
        "prompt": PROMPT_TEMPLATE.format(keyword=keyword),
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"[エラー] 記事生成失敗 ({keyword}): {e}")
        return None

def save_markdown(keyword, content):
    os.makedirs(POSTS_DIR, exist_ok=True)
    safe_keyword = keyword.replace(' ', '_').replace('/', '_')
    filename = os.path.join(POSTS_DIR, f"{safe_keyword}.md")
    
    if os.path.exists(filename):
        print(f"[スキップ] 既に存在します: {filename}")
        return False

    frontmatter = f"""---
title: "{keyword} のおすすめ比較・解説"
date: "{time.strftime('%Y-%m-%d')}"
draft: false
---

"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    print(f"[作成完了] {filename}")
    return True

def main():
    print("=== 自動生成パイプライン開始 ===")
    all_keywords = set()
    for seed in SEED_KEYWORDS:
        suggests = fetch_suggest_keywords(seed)
        all_keywords.update(suggests)
        time.sleep(1)

    print(f"[リサーチ結果] {len(all_keywords)} 個のキーワードを発見しました。")

    # 1回の実行で3記事生成
    for kw in list(all_keywords)[:3]:
        print(f"\n[処理中] キーワード: {kw}")
        article = generate_article(kw)
        if article:
            save_markdown(kw, article)

    print("\n=== 全処理が完了しました ===")

if __name__ == "__main__":
    main()