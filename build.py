import os
import glob
import re
import markdown

os.makedirs("posts", exist_ok=True)
md_files = glob.glob("posts/*.md")

AFFILIATE_URL = "https://px.a8.net/svt/ejp?a8mat=4BCNG8+BMJR1U+4JVQ+5YZ77"

def make_button_box(title_text="頭金0円・月々定額で人気の新車に乗れる！"):
    return f'''
<div style="text-align: center; margin: 32px 0; padding: 24px; background-color: #f0f9ff; border: 2px solid #bae6fd; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
    <div style="font-weight: bold; font-size: 1.1rem; color: #0369a1; margin-bottom: 12px;">【PR】{title_text}</div>
    <a href="{AFFILIATE_URL}" target="_blank" rel="nofollow" style="background-color: #0284c7; color: #ffffff; font-weight: bold; font-size: 1.05rem; padding: 14px 28px; border-radius: 8px; text-decoration: none; display: inline-block;">オリコで乗ーる 公式サイトで詳しく見る &rarr;</a>
</div>
'''

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
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: var(--bg-color); color: var(--text-main); line-height: 1.75; padding: 20px; }
        header { max-width: var(--max-width); margin: 40px auto 30px; text-align: center; }
        header a { font-size: 1.8rem; font-weight: 800; color: var(--text-main); text-decoration: none; letter-spacing: -0.025em; }
        header a:hover { color: var(--primary); }
        main { max-width: var(--max-width); margin: 0 auto 60px; }
        .post-grid { display: grid; gap: 20px; }
        .post-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 24px; transition: transform 0.2s ease, box-shadow 0.2s ease; text-decoration: none; color: inherit; display: block; }
        .post-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border-color: var(--primary); }
        .post-date { font-size: 0.85rem; color: var(--text-sub); margin-bottom: 8px; display: block; }
        .post-title { font-size: 1.25rem; font-weight: 700; line-height: 1.4; color: var(--text-main); }
        .article-container { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 32px; }
        .article-container h1 { font-size: 1.8rem; margin-bottom: 24px; line-height: 1.3; border-bottom: 2px solid var(--border); padding-bottom: 16px; }
        .article-container h2 { font-size: 1.4rem; margin: 32px 0 16px; padding-left: 12px; border-left: 4px solid var(--primary); }
        .article-container h3 { font-size: 1.15rem; margin: 24px 0 12px; }
        .article-container p { margin-bottom: 20px; word-break: break-word; }
        .article-container ul, .article-container ol { margin: 0 0 20px 24px; }
        .article-container li { margin-bottom: 6px; }
        .article-container blockquote { background: var(--bg-color); border-left: 4px solid var(--text-sub); padding: 12px 16px; margin-bottom: 20px; color: var(--text-sub); font-style: italic; }
        .back-link { display: inline-block; margin-bottom: 20px; color: var(--primary); text-decoration: none; font-weight: 600; }
        .back-link:hover { text-decoration: underline; }
        footer { max-width: var(--max-width); margin: 0 auto; text-align: center; font-size: 0.85rem; color: var(--text-sub); padding: 20px 0; border-top: 1px solid var(--border); }
    </style>
</head>
<body>
    <header><a href="/">Auto Tech Blog</a></header>
    <main>
"""

HTML_FOOT = """
    </main>
    <footer>&copy; Auto Tech Blog. All rights reserved.</footer>
</body>
</html>
"""

posts_data = []

for file_path in md_files:
    filename = os.path.basename(file_path).replace(".md", "")
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    clean_text = md_text
    if clean_text.startswith("---"):
        parts = clean_text.split("---", 2)
        if len(parts) >= 3:
            clean_text = parts[2].strip()

    lines = clean_text.splitlines()
    title = filename
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break

    # 見出し内の不要なタグを除去
    clean_text = re.sub(r'(#+)\s*\[AFFILIATE_LINK_\d+\]\s*:?\s*', r'\1 ', clean_text)

    html_content = markdown.markdown(clean_text, extensions=['fenced_code', 'tables'])

    has_button = False
    for i in range(1, 4):
        tag = f"[AFFILIATE_LINK_{i}]"
        if tag in html_content:
            html_content = html_content.replace(tag, make_button_box())
            has_button = True

    # 記事ページ（about以外）なら確実にボタンを挿入
    if filename != "about":
        if not has_button:
            if "</h2>" in html_content:
                parts = html_content.split("</h2>", 1)
                html_content = parts[0] + "</h2>\n" + make_button_box("おすすめの新車カーリース") + parts[1]
            else:
                html_content = make_button_box("おすすめの新車カーリース") + html_content

        # 記事末尾にもボタンを追加（成約率向上）
        html_content += make_button_box("頭金なし・月々定額で乗れる【オリコで乗ーる】")

    if filename.startswith("post_") and len(filename) >= 13:
        date_raw = filename.split("_")[1]
        date_str = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:8]}" if len(date_raw) >= 8 else "最新記事"
    elif filename == "about":
        date_str = "固定ページ"
    else:
        date_str = "最新記事"

    if filename != "about":
        posts_data.append({"title": title, "filename": f"{filename}.html", "date": date_str, "raw_filename": filename})

    article_html = f"{HTML_HEAD.replace('{{TITLE}}', title)}\n<a href='/' class='back-link'>&larr; 記事一覧へ戻る</a>\n<div class='article-container'>\n{html_content}\n</div>\n{HTML_FOOT}"

    with open(f"{filename}.html", "w", encoding="utf-8") as f:
        f.write(article_html)

posts_data.sort(key=lambda x: x["raw_filename"], reverse=True)

index_body = '<div class="post-grid">\n' + "".join([f'  <a href="{p["filename"]}" class="post-card"><span class="post-date">{p["date"]}</span><div class="post-title">{p["title"]}</div></a>\n' for p in posts_data]) + '</div>\n'
index_html = f"{HTML_HEAD.replace('{{TITLE}}', 'Auto Tech Blog')}\n{index_body}\n{HTML_FOOT}"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("Build completed successfully with guaranteed affiliate buttons.")
