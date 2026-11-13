import os, glob, markdown, json, re

POSTS_DIR = "posts"
OUTPUT_DIR = "public"
SITE_URL = "https://my-auto-blog.pages.dev"

CARNEXT_HTML = """
<div style="text-align: center; margin: 40px 0; padding: 25px; background: linear-gradient(135deg, #1e222d 0%, #2a2f3d 100%); border-radius: 12px; border-left: 6px solid #e60012; box-shadow: 0 8px 20px rgba(0,0,0,0.3); color: #fff;">
    <p style="font-weight: bold; font-size: 1.2em; color: #ff4d4d; margin-bottom: 15px; margin-top: 0;">＼ どんな車も高価買取！電話1本で無料査定 ／</p>
    <div style="margin-bottom: 15px;">
        <a href="https://px.a8.net/svt/ejp?a8mat=4BCEVJ+FH9R02+32YG+HYNBL" rel="nofollow" target="_blank">
        <img border="0" width="300" height="250" alt="カーネクスト" src="https://www24.a8.net/svt/bgt?aid=260919631936&wid=001&eno=01&mid=s00000014380003017000&mc=1" style="max-width: 100%; height: auto; border-radius: 8px;"></a>
    </div>
    <a href="https://px.a8.net/svt/ejp?a8mat=4BCEVJ+FH9R02+32YG+HYNBL" target="_blank" rel="nofollow noopener" style="display: inline-block; background: linear-gradient(90deg, #e60012 0%, #ff3300 100%); color: #ffffff; padding: 14px 32px; font-size: 1.1em; font-weight: 800; text-decoration: none; border-radius: 50px;">
        カーネクストで無料査定してみる 🚗💨
    </a>
</div>
"""

LEASE_HTML = """
<div style="text-align: center; margin: 40px 0; padding: 25px; background: linear-gradient(135deg, #1e222d 0%, #2a2f3d 100%); border-radius: 12px; border-left: 6px solid #e60012; box-shadow: 0 8px 20px rgba(0,0,0,0.3); color: #fff;">
    <p style="font-weight: bold; font-size: 1.25em; color: #ff4d4d; margin-bottom: 15px; margin-top: 0;">＼ 月々定額・頭金0円で話題の新車に乗れる！ ／</p>
    <a href="https://px.a8.net/svt/ejp?a8mat=YOUR_AFFILIATE_ID" target="_blank" rel="nofollow noopener" style="display: inline-block; background: linear-gradient(90deg, #e60012 0%, #ff3300 100%); color: #ffffff; padding: 16px 36px; font-size: 1.15em; font-weight: 800; text-decoration: none; border-radius: 50px;">
        オリコ「NORIKAE / ノール」の詳細を見る 🏎️💨
    </a>
</div>
"""

os.makedirs(OUTPUT_DIR, exist_ok=True)
posts_data, urls = [], [SITE_URL]

for file_path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 判定ロジック：ファイル名に lease が含まれていればリース、kaitori または 買取等が含まれていればカーネクスト
    if "lease" in file_path.lower():
        target_ad = LEASE_HTML
    elif any(k in text or k in file_path for k in ["kaitori", "買取", "査定", "売る", "売却", "事故車", "廃車", "買い替え", "中古車", "処分", "相場", "車検", "高価"]):
        target_ad = CARNEXT_HTML
    else:
        target_ad = CARNEXT_HTML  # デフォルトをカーネクストに変更

    text = text.replace("[AFFILIATE_LINK_1]", target_ad) if "[AFFILIATE_LINK_1]" in text else text + f"\n\n{target_ad}"
    html_content = markdown.markdown(text)
    
    title = next((l.replace("# ", "").strip() for l in text.strip().split("\n") if l.startswith("# ")), "無題の記事")
    base_filename = os.path.basename(file_path)
    date_match = re.search(r'(\d{4})(\d{2})(\d{2})', base_filename)
    date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}" if date_match else "2026-10-01"
    base_name = base_filename.replace(".md", ".html")

    page_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DRIVE & LEASE NAVI</title>
    <style>
        body {{ font-family: sans-serif; max-width: 900px; margin: 0 auto; padding: 0 15px 40px; background: #f0f2f5; color: #2b2b2b; line-height: 1.8; }}
        header {{ background: #12151c; margin: 0 -15px 30px; padding: 20px; text-align: center; border-bottom: 3px solid #e60012; }}
        .nav-back {{ color: #fff; text-decoration: none; font-weight: bold; background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 30px; }}
        main {{ background: #fff; padding: 40px; border-radius: 12px; }}
        .post-date {{ color: #e60012; font-weight: bold; background: #ffe6e6; padding: 2px 10px; border-radius: 4px; margin-bottom: 15px; display: inline-block; }}
        h1 {{ color: #111; border-left: 6px solid #e60012; padding-left: 15px; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; }}
    </style>
</head>
<body>
    <header><a href="index.html" class="nav-back">🏎️ トップページへ戻る</a></header>
    <main><span class="post-date">DATE: {date_str}</span>{html_content}</main>
</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, base_name), "w", encoding="utf-8") as f:
        f.write(page_html)
    posts_data.append({"title": title, "url": base_name, "date": date_str})
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
        body {{ font-family: sans-serif; max-width: 960px; margin: 0 auto; padding: 0 15px 50px; background: #0b0d12; color: #e0e0e0; }}
        header {{ text-align: center; padding: 45px 20px 35px; background: #1a1e29; margin: 0 -15px 30px; border-bottom: 3px solid #e60012; }}
        .badge {{ background: #e60012; color: #fff; font-size: 0.8em; font-weight: 900; padding: 4px 12px; border-radius: 3px; }}
        h1 {{ color: #fff; font-size: 2.2em; margin: 10px 0; }}
        .controls {{ display: flex; gap: 15px; margin-bottom: 35px; background: #161922; padding: 15px; border-radius: 10px; }}
        .search-box, .sort-select {{ flex: 1; padding: 12px; background: #0b0d12; border: 1px solid #3a4052; color: #fff; border-radius: 6px; outline: none; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 22px; }}
        .card {{ background: #1c202b; border-radius: 10px; padding: 22px; border: 1px solid #2a2f3e; text-decoration: none; color: inherit; display: flex; flex-direction: column; justify-content: space-between; transition: 0.3s; }}
        .card:hover {{ border-color: #e60012; transform: translateY(-3px); }}
        .card-date {{ color: #e60012; font-size: 0.8em; font-weight: bold; margin-bottom: 10px; }}
        .card-title {{ color: #fff; font-size: 1.1em; margin: 0 0 18px; }}
        .card-more {{ color: #a0a6b5; font-size: 0.85em; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <span class="badge">AUTOMOBILE & LEASE</span>
        <h1>DRIVE & LEASE NAVI</h1>
        <p>損しないクルマ選び・カーリース徹底比較ガイド</p>
    </header>
    <div class="controls">
        <input type="text" id="searchInput" class="search-box" placeholder="🔍 車種名やキーワードで記事を検索...">
        <select id="sortSelect" class="sort-select"><option value="newest">⏱️ 新しい順</option><option value="oldest">⌛ 古い順</option></select>
    </div>
    <div class="grid" id="postsGrid"></div>
    <script>
        const posts = {posts_json};
        const searchInput = document.getElementById('searchInput'), sortSelect = document.getElementById('sortSelect'), postsGrid = document.getElementById('postsGrid');
        function renderPosts() {{
            const query = searchInput.value.toLowerCase().trim();
            let filtered = posts.filter(p => p.title.toLowerCase().includes(query));
            filtered.sort((a, b) => sortSelect.value === 'newest' ? new Date(b.date) - new Date(a.date) : new Date(a.date) - new Date(b.date));
            postsGrid.innerHTML = filtered.length ? filtered.map(p => `<a href="${{p.url}}" class="card"><div><div class="card-date">DATE: ${{p.date}}</div><div class="card-title">${{p.title}}</div></div><div class="card-more">READ MORE →</div></a>`).join('') : '<div style=\"color:#888;grid-column:1/-1;text-align:center;padding:50px;\">該当する記事が見つかりませんでした。</div>';
        }}
        searchInput.addEventListener('input', renderPosts);
        sortSelect.addEventListener('change', renderPosts);
        renderPosts();
    </script>
</body>
</html>"""

with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap_xml += f'  <url><loc>{url}</loc></url>\n'
sitemap_xml += '</urlset>'

with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print("build.py updated successfully.")