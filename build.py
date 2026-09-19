import os
import glob
import re
import markdown

def clean_markdown(text):
    # AIが付ける ```markdown や ``` の囲み枠を完全除去
    text = re.sub(r'^```markdown\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
    return text

def build_site():
    posts_dir = "posts"
    md_files = glob.glob(os.path.join(posts_dir, "post_*.md"))
    md_files.sort(reverse=True)

    articles = []

    for filepath in md_files:
        filename = os.path.basename(filepath)
        html_filename = filename.replace(".md", ".html")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        content = clean_markdown(content)

        lines = content.splitlines()
        title = None
        body_lines = []
        
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("# ") and not title:
                title = line_str.replace("# ", "").strip()
            else:
                body_lines.append(line)

        # H1が見つからない場合は最初の文字行を使用
        if not title:
            for line in lines:
                if line.strip():
                    title = line.strip().replace("#", "").strip()
                    break

        if not title:
            title = "無題の記事"

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

    print("全記事の再ビルドが完了しました。")

if __name__ == "__main__":
    build_site()
