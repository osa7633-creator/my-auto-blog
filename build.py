import os
import glob
import markdown
import json
import re

POSTS_DIR = "posts"
OUTPUT_DIR = "public"
SITE_URL = "https://my-auto-blog.pages.dev"

AFFILIATE_URL = "https://px.a8.net/svt/ejp?a8mat=YOUR_AFFILIATE_ID"
AFFILIATE_HTML = f"""
<div style="text-align: center; margin: 40px 0; padding: 25px; background: linear-gradient(135deg, #1e222d 0%, #2a2f3d 100%); border-radius: 12px; border-left: 6px solid #e60012; box-shadow: 0 8px 20px rgba(0,0,0,0.3); color: #fff;">
    <p style="font-weight: bold; font-size: 1.25em; color: #ff4d4d; margin-bottom: 15px; margin-top: 0; letter-spacing: 0.05em;">＼ 月々定額・頭金0円で話題の新車に乗れる！ ／</p>
    <a href="{AFFILIATE_URL}" target="_blank" rel="nofollow noopener" style="display: inline-block; background: linear-gradient(90deg, #e60012 0%, #ff3300 100%); color: #ffffff; padding: 16px 36px; font-size: 1.15em; font-weight: 800; text-decoration: none; border-radius: 50px; box-shadow: 0 4px 15px rgba(230,0,18,0.4); transition: all 0.3s ease;">
        オリコ「NORIKAE / ノール」の詳細を見る 🏎️💨
    </a>
</div>
"""

os.makedirs(OUTPUT_DIR, exist_ok=True)

md_files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
posts_data = []
urls = [SITE_URL]

for file_path in md_files:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if "[AFFILIATE_LINK_1]" in text:
        text = text.replace("[AFFILIATE_LINK_1]", AFFILIATE_HTML)
    else:
        text += f"\n\n{AFFILIATE_HTML}"

    html_content = markdown.markdown(text)
    
    lines = text.strip().split("\n")
    title = "無題の記事"
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break

    base_filename = os.path.basename(file_path)
    date_match = re.search(r'(\d{4})(\d{2})(\d{2})', base_filename)
    if date_match:
        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    else:
        date_str = "2026-10-01"

    base_name = base_filename.replace(".md", ".html")
    out_path = os.path.join(OUTPUT_DIR, base_name)

    page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DRIVE & LEASE NAVI</title>
    <style>
        :root {{ --primary: #e60012; --dark: #12151c; --card-bg: #ffffff; --text: #2b2b2b; }}
        body {{ font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", sans-serif; max-width: 900px; margin: 0 auto; padding: 0 15px 40px; color: var(--text); background: #f0f2f5; line-height: 1.8; }}
        header {{ background: var(--dark); margin: 0 -15px 30px; padding: 20px; text-align: center; border-bottom: 3px solid var(--primary); box-shadow: 0 4px 10px rgba(0,0,0,0.15); }}
        .nav-back {{ display: inline-block; padding: 8px 20px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 30px; text-decoration: none; color: #fff; font-weight: bold; font-size: 0.9em; transition: 0.3s; }}
        .nav-back:hover {{ background: var(--primary); border-color: var(--primary); }}
        main {{ background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
        .post-date {{ color: #e60012; font-weight: bold; font-size: 0.9em; margin-bottom: 15px; display: inline-block; background: #ffe6e6; padding: 2px 10px; border-radius: 4px; }}
        h1 {{ color: #111; font-size: 1.8em; margin-top: 0; border-left: 6px solid var(--primary); padding-left: 15px; line-height: 1.4; }}
        h2 {{ color: #111; background: #f8f9fa; padding: 10px 15px; border-left: 4px solid var(--primary); border-bottom: 1px solid #e9ecef; margin-top: 35px; font-size: 1.3em; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" class="nav-back">🏎️ トップページへ戻る</a>
    </header>
    <main>
        <span class="post-date">DATE: {date_str}</span>
        {html_content}
    </main>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page_html)

    posts_data.append({
        "title": title,
        "url": base_name,
        "date": date_str
    })
    urls.append(f"{SITE_URL}/{base_name}")

posts_data.sort(key=lambda x: x["date"], reverse=True)
posts_json = json.dumps(posts_data, ensure_ascii=False)

index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DRIVE & LEASE NAVI | 愛車買取・カーリース徹底ガイド</title>
    <style>
        :root {{ --primary: #e60012; --dark: #12151c; --bg: #0b0d12; --card-bg: #1c202b; }}
        body {{ font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", sans-serif; max-width: 960px; margin: 0 auto; padding: 0 15px 50px; background: var(--bg); color: #e0e0e0; }}
        header {{ text-align: center; padding: 45px 20px 35px; background: linear-gradient(180deg, #1a1e29 0%, #0b0d12 100%); margin: 0 -15px 30px; border-bottom: 3px solid var(--primary); position: relative; overflow: hidden; }}
        header::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(45deg, rgba(230,0,18,0.03), rgba(230,0,18,0.03) 10px, transparent 10px, transparent 20px); pointer-events: none; }}
        .badge {{ display: inline-block; background: var(--primary); color: #fff; font-size: 0.8em; font-weight: 900; padding: 4px 12px; border-radius: 3px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; box-shadow: 0 0 10px rgba(230,0,18,0.5); }}
        h1 {{ font-size: 2.2em; color: #ffffff; margin: 0 0 10px; font-weight: 800; letter-spacing: 0.03em; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }}
        .subtitle {{ color: #a0a6b5; font-size: 0.95em; margin: 0; }}
        .controls {{ display: flex; gap: 15px; margin-bottom: 35px; flex-wrap: wrap; background: #161922; padding: 15px; border-radius: 10px; border: 1px solid #2a2f3e; }}
        .search-box {{ flex: 1; min-width: 220px; padding: 12px 18px; background: #0b0d12; border: 1px solid #3a4052; border-radius: 6px; font-size: 0.95em; color: #fff; outline: none; }}
        .search-box:focus {{ border-color: var(--primary); box-shadow: 0 0 8px rgba(230,0,18,0.3); }}
        .sort-select {{ padding: 12px 18px; background: #0b0d12; border: 1px solid #3a4052; border-radius: 6px; font-size: 0.95em; color: #fff; cursor: pointer; outline: none; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 22px; }}
        .card {{ background: var(--card-bg); border-radius: 10px; padding: 22px; border: 1px solid #2a2f3e; transition: all 0.3s ease; text-decoration: none; color: inherit; display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden; }}
        .card::before {{ content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #3a4052; transition: 0.3s; }}
        .card:hover {{ transform: translateY(-5px); border-color: var(--primary); box-shadow: 0 8px 25px rgba(230,0,18,0.25); }}
        .card:hover::before {{ background: var(--primary); }}
        .card-date {{ font-size: 0.8em; color: #e60012; font-weight: bold; margin-bottom: 10px; letter-spacing: 0.05em; }}
        .card-title {{ font-size: 1.1em; font-weight: 700; line-height: 1.5; color: #ffffff; margin: 0 0 18px; }}
        .card-more {{ font-size: 0.85em; color: #a0a6b5; font-weight: bold; margin-top: auto; display: flex; align-items: center; gap: 5px; }}
        .card:hover .card-more {{ color: var(--primary); }}
        .no-results {{ text-align: center; color: #888; grid-column: 1 / -1; padding: 50px; background: #161922; border-radius: 10px; }}
    </style>
</head>
<body>
    <header>
        <span class="badge">AUTOMOBILE & LEASE</span>
        <h1>DRIVE & LEASE NAVI</h1>
        <p class="subtitle">損しないクルマ選び・カーリース徹底比較ガイド</p>
    </header>

    <div class="controls">
        <input type="text" id="searchInput" class="search-box" placeholder="🔍 車種名やキーワードで記事を検索...">
        <select id="sortSelect" class="sort-select">
            <option value="newest">⏱️ 新しい順</option>
            <option value="oldest">⌛ 古い順</option>
        </select>
    </div>

    <div class="grid" id="postsGrid"></div>

    <script>
        const posts = {posts_json};
        const searchInput = document.getElementById('searchInput');
        const sortSelect = document.getElementById('sortSelect');
        const postsGrid = document.getElementById('postsGrid');

        function renderPosts() {{
            const query = searchInput.value.toLowerCase().trim();
            const sortOrder = sortSelect.value;

            let filtered = posts.filter(post => post.title.toLowerCase().includes(query));

            filtered.sort((a, b) => {{
                if (sortOrder === 'newest') return new Date(b.date) - new Date(a.date);
                if (sortOrder === 'oldest') return new Date(a.date) - new Date(a.date);
            }});

            if (filtered.length === 0) {{
                postsGrid.innerHTML = '<div class="no-results">該当する記事が見つかりませんでした。</div>';
                return;
            }}

            postsGrid.innerHTML = filtered.map(post => `
                <a href="${{post.url}}" class="card">
                    <div>
                        <div class="card-date">DATE: ${{post.date}}</div>
                        <h2 class="card-title">${{post.title}}</h2>
                    </div>
                    <div class="card-more">READ MORE <span>→</span></div>
                </a>
            `).join('');
        }}

        searchInput.addEventListener('input', renderPosts);
        sortSelect.addEventListener('change', renderPosts);

        renderPosts();
    </script>
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

print("Updated build.py successfully")
