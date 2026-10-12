import os
import glob
import markdown

POSTS_DIR = "posts"
OUTPUT_DIR = "public"
SITE_URL = "https://my-auto-blog.pages.dev"

# ▼ ここにご自身のアフィリエイトURL（またはボタンHTML）を設定します
# 例: A8.net などの計測用URL
AFFILIATE_URL = "https://px.a8.net/svt/ejp?a8mat=YOUR_AFFILIATE_ID"

# ボタン形式のアフィリエイトHTMLコンポーネント
AFFILIATE_HTML = f"""
<div style="text-align: center; margin: 30px 0; padding: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;">
    <p style="font-weight: bold; font-size: 1.1em; margin-bottom: 15px;">＼ 月々定額・頭金なしで新車に乗れる！ ／</p>
    <a href="{AFFILIATE_URL}" target="_blank" rel="nofollow noopener" style="display: inline-block; background-color: #ff6b00; color: #ffffff; padding: 15px 30px; font-size: 1.2em; font-weight: bold; text-decoration: none; border-radius: 50px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        オリコ「NORIKAE / ノール」の詳細を見る →
    </a>
</div>
"""

os.makedirs(OUTPUT_DIR, exist_ok=True)

md_files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
posts = []
urls = [SITE_URL]

for file_path in md_files:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # [AFFILIATE_LINK_1] をボタンHTMLへ自動置換
    if "[AFFILIATE_LINK_1]" in text:
        text = text.replace("[AFFILIATE_LINK_1]", AFFILIATE_HTML)
    else:
        # タグが存在しない場合の末尾フォールバック挿入
        text += f"\n\n{AFFILIATE_HTML}"

    html_content = markdown.markdown(text)
    
    lines = text.strip().split("\n")
    title = "無題の記事"
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break

    base_name = os.path.basename(file_path).replace(".md", ".html")
    out_path = os.path.join(OUTPUT_DIR, base_name)

    page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }}
        a {{ color: #0066cc; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <a href="index.html">← トップへ戻る</a>
    <hr>
    {html_content}
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page_html)

    posts.append({"title": title, "url": base_name})
    urls.append(f"{SITE_URL}/{base_name}")

index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>愛車買取・カーリース徹底ガイド</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        li {{ margin-bottom: 10px; }}
    </style>
</head>
<body>
    <h1>愛車買取・カーリース徹底ガイド</h1>
    <ul>
"""
for p in posts:
    index_html += f'        <li><a href="{p["url"]}">{p["title"]}</a></li>\n'

index_html += """    </ul>
</body>
</html>"""

with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap_xml += f'  <url><loc>{url}</loc></url>\n'
sitemap_xml += '</urlset>'

with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("アフィリエイトリンクの置き換えとサイト構築が完了しました。")
