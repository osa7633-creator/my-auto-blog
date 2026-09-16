import os
import glob
import markdown

# 記事が入っているフォルダ
POSTS_DIR = "posts"

# Webページの見た目の枠組み（HTMLテンプレート）
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.8; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        h1, h2, h3 {{ color: #2b542c; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .header {{ margin-bottom: 30px; }}
        .card {{ border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #fafafa; }}
    </style>
</head>
<body>
    <div class="header">
        <a href="/">🏠 ブログトップへ戻る</a>
    </div>
    {content}
</body>
</html>
"""

def generate():
    # posts フォルダ内の .md ファイルをすべて探す
    md_files = glob.glob(f"{POSTS_DIR}/*.md")
    articles = []

    for file_path in md_files:
        filename = os.path.basename(file_path)
        title = os.path.splitext(filename)[0]

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # MarkdownテキストをHTMLコードに変換
        html_body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        
        # テンプレートに流し込む
        full_html = HTML_TEMPLATE.format(title=title, content=html_body)

        # .html ファイルとして保存する
        output_path = os.path.join(POSTS_DIR, f"{title}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        articles.append((title, f"{title}.html"))

    # トップページ（index.html）を作る
    index_body = "<h1>おすすめ車ガイドブログ</h1><h2>記事一覧</h2>"
    for title, link in articles:
        index_body += f'<div class="card"><h3><a href="{link}">{title}</a></h3></div>'

    full_index = HTML_TEMPLATE.format(title="おすすめ車ガイドブログ", content=index_body)
    
    # posts/index.html として保存
    with open(os.path.join(POSTS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(full_index)

    print("✅ 変換成功: .html ファイルと index.html を作成しました！")

if __name__ == "__main__":
    generate()