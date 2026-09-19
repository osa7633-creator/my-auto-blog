import os
import glob
import re
import markdown

def clean_content(text):
    text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

def extract_title_and_body(content):
    lines = content.splitlines()
    title = None
    body_lines = []

    filename_pattern = re.compile(r'^#?\s*post_\d{8}_\d{6}.*', re.IGNORECASE)

    for line in lines:
        stripped = line.strip()
        
        # post_2026... のようなファイル名行はタイトルとして無視する
        if not title and filename_pattern.match(stripped):
            continue

        # 最初に出てくる意味のある文字行をタイトルとして取得
        if not title and stripped:
            clean_title = re.sub(r'^[#\s\*=]+', '', stripped).strip()
            clean_title = re.sub(r'[\*=]+$', '', clean_title).strip()
            
            if clean_title:
                title = clean_title
                continue

        body_lines.append(line)

    if not title:
        title = "無題の記事"

    body_markdown = "\n".join(body_lines)
    return title, body_markdown

def build_site():
    posts_dir = "posts"
    md_files = glob.glob(os.path.join(posts_dir, "post_*.md"))
    md_files.sort(reverse=True)

    articles = []

    print("--- 記事タイトルの抽出結果 ---")
    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_content(content)
        title, body_markdown = extract_title_and_body(content)
        print(f"[{filename}] -> {title}")

        body_html = markdown.markdown(body_markdown)

        page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ font-size: 1.8em; color: #111; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .back-link {{ margin-bottom: 20px; display: inline-block; }}
    </style>
</head>
<body>
    <a href="../index.html" class="back-link">← トップページに戻る</a>
    <h1>{title}</h1>
    {body_html}
</body>
</html>"""

        with open(os.path.join(posts_dir, html_filename), "w", encoding="utf-8") as f:
            f.write(page_html)

        articles.append({
            "title": title,
            "url": f"posts/{html_filename}"
        })

    list_items = "".join([f'<li><a href="{a["url"]}">{a["title"]}</a></li>' for a in articles])
    
    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>愛車査定・買取攻略ブログ</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ font-size: 2em; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 15px; font-size: 1.1em; }}
        a {{ color: #0066cc; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>愛車査定・買取攻略ブログ</h1>
    <h2>最新の記事</h2>
    <ul>
        {list_items}
    </ul>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("--------------------------------")
    print("全記事の再ビルドが完了しました。")

if __name__ == "__main__":
    build_site()
