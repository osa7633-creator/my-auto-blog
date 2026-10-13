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
<div style="text-align: center; margin: 40px 0; padding: 25px; background: linear-gradient(135deg, #fff5eb 0%, #ffe8d6 100%); border-radius: 12px; border: 2px solid #ff6b00; box-shadow: 0 4px 12px rgba(255,107,0,0.15);">
    <p style="font-weight: bold; font-size: 1.25em; color: #d95300; margin-bottom: 15px; margin-top: 0;">＼ 月々定額・頭金なしで新車に乗れる！ ／</p>
    <a href="{AFFILIATE_URL}" target="_blank" rel="nofollow noopener" style="display: inline-block; background-color: #ff6b00; color: #ffffff; padding: 16px 36px; font-size: 1.2em; font-weight: bold; text-decoration: none; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,107,0,0.3); transition: transform 0.2s;">
        オリコ「NORIKAE / ノール」の詳細を見る →
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

    # アフィリエイトリンク置換
    if "[AFFILIATE_LINK_1]" in text:
        text = text.replace("[AFFILIATE_LINK_1]", AFFILIATE_HTML)
    else:
        text += f"\n\n{AFFILIATE_HTML}"

    html_content = markdown.markdown(text)
    
    # タイトルと日付の抽出
    lines = text.strip().split("\n")
    title = "無題の記事"
    for line in lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break

    # ファイル名から日付（YYYYMMDD）を抽出（例: post_20261012_010233.md -> 2026-10-12）
    base_filename = os.path.basename(file_path)
    date_match = re.search(r'(\d{4})(\d{2})(\d{2})', base_filename)
    if date_match:
        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
    else:
        date_str = "2026-10-01"

    base_name = base_filename.replace(".md", ".html")
    out_path = os.path.join(OUTPUT_DIR, base_name)

    # 記事ページの出力
    page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 愛車買取・カーリース徹底ガイド</title>
    <style>
        :root {{ --primary: #0066cc; --bg: #f8f9fa; --text: #333; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 850px; margin: 0 auto; padding: 20px; color: var(--text); background: var(--bg); line-height: 1.8; }}
        header {{ margin-bottom: 30px; text-align: center; }}
        .nav-back {{ display: inline-block; padding: 8px 16px; background: #fff; border-radius: 20px; text-decoration: none; color: var(--primary); font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        main {{ background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .post-date {{ color: #777; font-size: 0.9em; margin-bottom: 20px; }}
        h1 {{ color: #111; font-size: 1.8em; margin-top: 0; border-bottom: 2px solid var(--primary); padding-bottom: 10px; }}
        h2 {{ color: #222; border-left: 4px solid var(--primary); padding-left: 10px; margin-top: 30px; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; }}
    </style>
</head>
<body>
    <header>
        <a href="index.html" class="nav-back">← トップページへ戻る</a>
    </header>
    <main>
        <div class="post-date">公開日: {date_str}</div>
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

# 日付順（新しい順）にデフォルトソート
posts_data.sort(key=lambda x: x["date"], reverse=True)

# トップページ (index.html) の生成
posts_json = json.dumps(posts_data, ensure_ascii=False)

index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>愛車買取・カーリース徹底ガイド</title>
    <style>
        :root {{ --primary: #0066cc; --bg: #f4f6f9; --card-bg: #ffffff; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: var(--bg); color: #333; }}
        header {{ text-align: center; margin-bottom: 30px; padding: 20px 0; }}
        h1 {{ font-size: 2.2em; color: #111; margin-bottom: 10px; }}
        .subtitle {{ color: #666; font-size: 0.95em; }}
        
        /* 検索・ソートコントロール */
        .controls {{ display: flex; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .search-box {{ flex: 1; min-width: 200px; padding: 12px 16px; border: 1px solid #ccc; border-radius: 8px; font-size: 1em; outline: none; }}
        .search-box:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(0,102,204,0.1); }}
        .sort-select {{ padding: 12px 16px; border: 1px solid #ccc; border-radius: 8px; font-size: 1em; background: #fff; cursor: pointer; }}

        /* グリッドレイアウト */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .card {{ background: var(--card-bg); border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; color: inherit; display: flex; flex-direction: column; justify-content: space-between; }}
        .card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); }}
        .card-date {{ font-size: 0.85em; color: #888; margin-bottom: 8px; }}
        .card-title {{ font-size: 1.1em; font-weight: bold; line-height: 1.4; color: #1a1a1a; margin: 0 0 15px 0; }}
        .card-more {{ font-size: 0.9em; color: var(--primary); font-weight: bold; margin-top: auto; }}
        .no-results {{ text-align: center; color: #888; grid-column: 1 / -1; padding: 40px; }}
    </style>
</head>
<body>
    <header>
        <h1>愛車買取・カーリース徹底ガイド</h1>
        <p class="subtitle">損しないクルマ選びとおすすめカーリースの比較情報サイト</p>
    </header>

    <div class="controls">
        <input type="text" id="searchInput" class="search-box" placeholder="キーワードで記事を検索...">
        <select id="sortSelect" class="sort-select">
            <option value="newest">新しい順</option>
            <option value="oldest">古い順</option>
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
                        <div class="card-date">${{post.date}}</div>
                        <h2 class="card-title">${{post.title}}</h2>
                    </div>
                    <div class="card-more">記事を読む →</div>
                </a>
            `).join('');
        }}

        searchInput.addEventListener('input', renderPosts);
        sortSelect.addEventListener('change', renderPosts);

        // 初回レンダリング
        renderPosts();
    </script>
</body>
</html>"""

with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# sitemap.xml の更新
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap_xml += f'  <url><loc>{url}</loc></url>\n'
sitemap_xml += '</urlset>'

with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("新デザイン・検索・ソート機能付きサイトの構築が完了しました。")
