import os
import glob
import re
import markdown

def fix_and_clean_md(filepath):
    """ Markdownファイル内の先頭ゴミ文字列を直接除去して綺麗にする """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # コードブロック装飾の除去
    content = re.sub(r'^```markdown\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)

    lines = content.splitlines()
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        # ファイル名IDや単発の不要な文字列を削除
        if re.search(r'post_\d{8}_\d{6}', stripped, re.IGNORECASE):
            continue
        if stripped in ["レビューは", "選び方_公式"]:
            continue
        cleaned_lines.append(line)

    cleaned_content = "\n".join(cleaned_lines).strip()

    # 掃除した内容でMarkdownファイルを直接上書き保存
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

    return cleaned_content

def extract_title(content):
    lines = content.splitlines()
    
    # 1. '# ' (H1) から日本語のまともなタイトルを探す
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            title = re.sub(r'[\*=]+$', '', title).strip()
            if title and len(title) > 3 and not re.search(r'post_\d{8}', title):
                return title

    # 2. 見つからない場合、本文中で一番長い文章行を取得
    for line in lines:
        stripped = line.strip()
        cleaned = re.sub(r'^[#\s\*=]+', '', stripped).strip()
        if len(cleaned) >= 10 and not re.search(r'post_\d{8}', cleaned):
            return cleaned

    return "無題の記事"

def build_site():
    posts_dir = "posts"
    md_files = glob.glob(os.path.join(posts_dir, "post_*.md"))
    md_files.sort(reverse=True)

    articles = []

    print("=== 全記事のクレンジング & 再構築 ===")
    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        
        # 1. mdファイル自体のゴミ清掃
        content = fix_and_clean_md(filepath)
        
        # 2. タイトル抽出
        title = extract_title(content)
        print(f"[{filename}] -> {title}")

        # 3. 本文HTML作成 (タイトル行の重複を排除)
        body_lines = [l for l in content.splitlines() if title not in l]
        body_markdown = "\n".join(body_lines)
        body_html = markdown.markdown(body_markdown)

        # 個別記事HTML
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

    # カード型トップページHTML
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

    print("処理が正常終了しました。")

if __name__ == "__main__":
    build_site()
