import os
import glob
import markdown

POSTS_DIR = "posts"
OUTPUT_DIR = "public"
SITE_URL = "https://my-auto-blog.pages.dev"

os.makedirs(OUTPUT_DIR, exist_ok=True)

md_files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
posts = []
urls = [SITE_URL]

for file_path in md_files:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

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
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        a {{ color: #0066cc; }}
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

print("sitemap.xml の生成が完了しました。")
