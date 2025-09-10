import sqlite3

# --- ここに、残しておきたい投稿データをリストとして定義 ---
initial_posts = [
    {
        "content": "性格として、陽キャ、陰キャはある。だがそこに優劣はない。",
        "likes": 5
    },
    {
        "content": "挨拶を返せなかった理由を探している時が、一番ダサい。",
        "likes": 12
    },
    {
        "content": "全員が一抹の優しさを持ったら、世界はずっと良くなるのに。",
        "likes": 10
    },
    {
        "content": "この世界は、死ぬにはもったいないくらい、面白すぎる。",
        "likes": 1
    },
    {
        "content": "私は美しい人間だから、バイトだって辞めてもいい。",
        "likes": 30
    },
    {
        "content": "結局、美味しいご飯を食べていれば、人間は幸せでいられるのだ。",
        "likes": 15
    },
    # --- もし追加したい投稿があれば、この形式で追記できます ---
    # {
    #     "content": "新しい格言を追加します。",
    #     "likes": 0
    # },
]

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# forループを使って、リストの中身を一つずつデータベースに挿入
for post in initial_posts:
    cur.execute("INSERT INTO posts (content, likes) VALUES (?, ?)",
                (post['content'], post['likes'])
                )

connection.commit()
connection.close()

print("データベースが初期化され、サンプルデータが投入されました。")