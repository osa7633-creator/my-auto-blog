import os
import datetime

def create_post():
    print("=== DRIVE & LEASE NAVI 記事ジェネレーター ===")
    title = input("記事のタイトルを入力してください: ").strip()
    if not title:
        print("タイトルが入力されませんでした。中止します。")
        return

    # キーワードから自動でファイル名のプレフィックスや分類を決める補助
    is_lease = input("カーリース系の記事ですか？ (y/n): ").strip().lower() == 'y'
    prefix = "lease" if is_lease else "kaitori"

    today = datetime.date.today().strftime("%Y%m%d")
    filename = f"{today}_{prefix}_{title.replace(' ', '_').lower()}.md"
    filepath = os.path.join("posts", filename)

    os.makedirs("posts", exist_ok=True)

    content = f"""# {title}

ここに導入文を記述します。車の買い替え、査定、あるいはカーリースに関する最新情報をお届けします。

## 記事のポイント
- ポイント1
- ポイント2
- ポイント3

[AFFILIATE_LINK_1]
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ 新しい記事を作成しました: {filepath}")

if __name__ == "__main__":
    create_post()
