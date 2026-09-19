import os
import glob
import re
import markdown

def clean_content(text):
    # ```markdown などのコードブロック装飾を除去
    text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

def extract_real_title(content, filename):
    lines = content.splitlines()
    
    # 1. まず '# ' (H1タグ) で始まる行をすべて探す
    h1_candidates = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            # '# ' を取り除いた純粋なタイトル文字列
            title_text = stripped[2:].strip()
            title_text = re.sub(r'[\*=]+$', '', title_text).strip()
            h1_candidates.append(title_text)

    # H1候補の中から 'post_' や日付数字(8桁)を含まない本物のタイトルを選ぶ
    for cand in h1_candidates:
        if not re.search(r'post_\d{8}', cand, re.IGNORECASE) and not re.search(r'^\d{8}_\d{6}', cand):
            if len(cand) > 0:
                return cand

    # 2. H1タグで見つからなかった場合、全行から 'post_' や日付を含まない最もタイトルのような行を探す
    for line in lines:
        stripped = line.strip()
        cleaned = re.sub(r'^[#\s\*=]+', '', stripped).strip()
        cleaned = re.sub(r'[\*=]+$', '', cleaned).strip()
        
        if cleaned and not re.search(r'post_\d{8}', cleaned, re.IGNORECASE) and not re.search(r'^\d{8}_\d{6}', cleaned):
            # 日本語が含まれているか、または十分な長さがある行を採用
            if len(cleaned) >= 5:
                return cleaned

    return "無題の記事"

def build_site():
    posts_dir = "posts"
    md_files = glob.glob(os.path.join(posts_dir, "post_*.md"))
    md_files.sort(reverse=True)

    articles = []

    print("========================================")
    print(" 記事タイトルの抽出チェック結果")
    print("========================================")

    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_content(content)
        title = extract_real_title(content, filename)
        
        print(f"ファイル名: {filename}")
        print(f"抽出タイトル: {title}")
        print("-" * 40)

        # 本文用のMarkdown（H1タイトル重複防止のため、抽出タイトル行を除外してHTML化）
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

    print("全記事およびindex.htmlの再構築が完了しました。")

if __name__ == "__main__":
    build_site()
