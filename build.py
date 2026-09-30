import os
import glob
import re
import markdown

os.makedirs("posts", exist_ok=True)
md_files = glob.glob("posts/*.md")

# HTML共通テンプレート
HTML_HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-sub: #64748b;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --border: #e2e8f0;
            --max-width: 800px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.75;
            padding: 20px;
        }

        header {
            max-width: var(--max-width);
            margin: 40px auto 30px;
            text-align: center;
        }

        header a {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-main);
            text-decoration: none;
            letter-spacing: -0.025em;
        }

        header a:hover {
            color: var(--primary);
        }

        main {
            max-width: var(--max-width);
            margin: 0 auto 60px;
        }

        /* 記事一覧（カード型） */
        .post-grid {
            display: grid;
            gap: 20px;
        }

        .post-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .post-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            border-color: var(--primary);
        }

        .post-date {
            font-size: 0.85rem;
            color: var(--text-sub);
            margin-bottom: 8px;
            display: block;
        }

        .post-title {
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.4;
            color: var(--text-main);
        }

        /* 記事本文 */
        .article-container {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 32px;
        }

        .article-container h1 {
            font-size: 1.8rem;
            margin-bottom: 24px;
            line-height: 1.3;
            border-bottom: 2px solid var(--border);
            padding-bottom: 16px;
        }

        .article-container h2 {
            font-size: 1.4rem;
            margin: 32px 0 16px;
            padding-left: 12px;
            border-left: 4px solid var(--primary);
        }

        .article-container h3 {
            font-size: 1.15rem;
            margin: 24px 0 12px;
        }

        .article-container p {
            margin-bottom: 20px;
            word-break: break-word;
        }

        .article-container ul, .article-container ol {
            margin: 0 0 20px 24px;
        }

        .article-container li {
            margin-bottom: 6px;
        }

        .article-container blockquote {
            background: var(--bg-color);
            border-left: 4px solid var(--text-sub);
            padding: 12px 16px;
            margin-bottom: 20px;
            color: var(--text-sub);
            font-style: italic;
        }

        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
        }

        .back-link:hover {
            text-decoration: underline;
        }

        footer {
            max-width: var(--max-width);
            margin: 0 auto;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-sub);
            padding: 20px 0;
            border-top: 1px solid var(--border);
        }
    </style>
</head>
<body>
    <header>
        <a href="/">Auto Tech Blog</a>
    </header>
    <main>
"""

HTML_FOOT = """
    </main>
    <footer>
        &copy; Auto Tech Blog. All rights reserved.
    </footer>
</body>
</html>
"""

posts_data = []

for file_path in md_files:
    filename = os.path.basename(file_path).replace(".md", "")
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Front Matter (--- で囲まれたメタデータ) を除去
    clean_text = md_text
    if clean_text.startswith("---"):
        parts = clean_text.split("---", 2)
        if len(parts) >= 3:
            clean_text = parts[2].strip()

    # 未置換プレースホルダーのクリーンアップ
    clean_text = re.sub(r'\[AFFILIATE_LINK_\d+\]', '', clean_text)

    # タイトル抽出 (# 見出し)
    lines = clean_text.splitlines()
    title = filename
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break

    # 日付抽出 (post_YYYYMMDD_... から判定)
    if filename.startswith("post_") and len(filename) >= 13:
        date_raw = filename.split("_")[1]
        if len(date_raw) >= 8:
            date_str = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:8]}"
        else:
            date_str = "最新記事"
    else:
        date_str = "最新記事"

    html_body = markdown.markdown(clean_text, extensions=['fenced_code', 'tables'])

    posts_data.append({
        "title": title,
        "filename": f"{filename}.html",
        "date": date_str,
        "raw_filename": filename
    })

    article_head = HTML_HEAD.replace("{{TITLE}}", title)
    article_html = f"{article_head}\n"
    article_html += '<a href="/" class="back-link">&larr; 記事一覧へ戻る</a>\n'
    article_html += f'<div class="article-container">\n{html_body}\n</div>\n'
    article_html += HTML_FOOT

    with open(f"{filename}.html", "w", encoding="utf-8") as f:
        f.write(article_html)

posts_data.sort(key=lambda x: x["raw_filename"], reverse=True)

index_body = '<div class="post-grid">\n'
for post in posts_data:
    index_body += f'''  <a href="{post['filename']}" class="post-card">
    <span class="post-date">{post['date']}</span>
    <div class="post-title">{post['title']}</div>
  </a>\n'''
index_body += '</div>\n'

index_head = HTML_HEAD.replace("{{TITLE}}", "Auto Tech Blog")
index_html = f"{index_head}\n{index_body}\n{HTML_FOOT}"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("Build completed successfully.")
