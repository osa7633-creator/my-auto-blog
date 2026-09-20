import os
import glob
import re
import markdown

def clean_content(text):
    text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

def extract_real_title(content, filename):
    lines = content.splitlines()
    
    # 1. '# ' (H1) から post_ や日付以外の純粋なタイトルを探す
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title_text = stripped[2:].strip()
            title_text = re.sub(r'[\*=]+$', '', title_text).strip()
            if title_text and not re.search(r'post_\d{8}', title_text, re.IGNORECASE) and not re.search(r'^\d{8}_\d{6}', title_text):
                return title_text

    # 2. H1で見つからない場合、本文全体から一番それっぽい行を探す
    for line in lines:
        stripped = line.strip()
        cleaned = re.sub(r'^[#\s\*=]+', '', stripped).strip()
        cleaned = re.sub(r'[\*=]+$', '', cleaned).strip()
        
        if cleaned and not re.search(r'post_\d{8}', cleaned, re.IGNORECASE) and not re.search(r'^\d{8}_\d{6}', cleaned):
            if len(cleaned) >= 5 and "ブログ" not in cleaned and "トップ" not in cleaned:
                return cleaned

    return "無題の記事"

def build_site():
    posts_dir = "posts"
    md_files = glob.glob(os.path.join(posts_dir, "post_*.md"))
    md_files.sort(reverse=True)

    articles = []

    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_content(content)
        title = extract_real_title(content, filename)

        body_lines = [l for l in content.splitlines() if title not in l and not re.search(r'post_\d{8}', l, re.IGNORECASE)]
        body_markdown = "\n".join(body_lines)
        body_html = markdown.markdown(body_markdown)

        page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; background-color: #fcfcfc; }}
        .header-nav {{ margin-bottom: 20px; }}
        .header-nav a {{ color: #0066cc; text-decoration: none; font-size: 0.9em; }}
        h1 {{ font-size: 1.8em; color: #111; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 10px; }}
        .content {{ background: #fff; padding: 25px; border-radius: 8px; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
    </style>
</head>
<body>
    <div class="header-nav"><a href="../index.html">🏠 ブログトップへ戻る</a></div>
    <div class="content">
        <h1>{title}</h1>
        {body_html}
    </div>
</body>
</html>"""

        with open(os.path.join(posts_dir, html_filename), "w", encoding="utf-8") as f:
            f.write(page_html)

        articles.append({
            "title": title,
            "url": f"posts/{html_filename}"
        })

    cards_html = ""
    for a in articles:
        cards_html += f"""
        <a href="{a['url']}" class="card-link">
            <div class="card">
                <h3>{a['title']}</h3>
            </div>
        </a>"""

    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>おすすめ車ガイドブログ</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #1e3a1e; background-color: #fff; }}
        .header-nav {{ margin-bottom: 15px; }}
        .header-nav a {{ color: #0066cc; text-decoration: none; font-size: 0.9em; }}
        h1 {{ font-size: 2.2em; color: #1e3a1e; margin-bottom: 20px; border-bottom: 2px solid #eef2ee; padding-bottom: 10px; }}
        h2 {{ font-size: 1.4em; color: #1e3a1e; margin-top: 20px; margin-bottom: 15px; }}
        .card-container {{ display: flex; flex-direction: column; gap: 15px; }}
        .card-link {{ text-decoration: none; color: inherit; display: block; }}
        .card {{ background: #f9f9f9; border: 1px solid #eee; border-radius: 8px; padding: 20px; transition: transform 0.1s ease, box-shadow 0.1s ease; }}
        .card:hover {{ background: #f4f6f4; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.05); }}
        .card h3 {{ margin: 0; color: #0055aa; font-size: 1.1em; line-height: 1.4; }}
    </style>
</head>
<body>
    <div class="header-nav"><a href="index.html">🏠 ブログトップへ戻る</a></div>
    <h1>おすすめ車ガイドブログ</h1>
    <h2>記事一覧</h2>
    <div class="card-container">
        {cards_html}
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("全記事の再構築が完了しました。")

if __name__ == "__main__":
    build_site()
