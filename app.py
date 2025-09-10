import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    sort_by = request.args.get('sort', 'newest')
    conn = get_db_connection()
    if sort_by == 'likes':
        posts = conn.execute('SELECT * FROM posts ORDER BY likes DESC, created DESC').fetchall()
    elif sort_by == 'reports':
        posts = conn.execute('SELECT * FROM posts ORDER BY reports DESC, created DESC').fetchall()
    else:
        posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, sort_by=sort_by)

@app.route("/create", methods=['POST'])
def create():
    content = request.form['content']
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (content, likes, reports) VALUES (?, ?, ?)', (content, 0, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT likes FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post:
        new_likes = post['likes'] + 1
        conn.execute('UPDATE posts SET likes = ? WHERE id = ?', (new_likes, post_id))
        conn.commit()
        conn.close()
        return jsonify({'likes': new_likes})
    return jsonify({'error': 'Post not found'}), 404

@app.route('/unlike/<int:post_id>', methods=['POST'])
def unlike(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT likes FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post:
        if post['likes'] > 0:
            new_likes = post['likes'] - 1
            conn.execute('UPDATE posts SET likes = ? WHERE id = ?', (new_likes, post_id))
            conn.commit()
        else:
            new_likes = 0
        conn.close()
        return jsonify({'likes': new_likes})
    return jsonify({'error': 'Post not found'}), 404

@app.route('/report/<int:post_id>', methods=['POST'])
def report(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT reports FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post:
        new_reports = post['reports'] + 1
        conn.execute('UPDATE posts SET reports = ? WHERE id = ?', (new_reports, post_id))
        conn.commit()
        conn.close()
        return jsonify({'reports': new_reports})
    return jsonify({'error': 'Post not found'}), 404

# --- ↓ここを修正！↓ ---
@app.route('/unreport/<int:post_id>', methods=['POST'])
def unreport(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT reports FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post:
        if post['reports'] > 0:
            new_reports = post['reports'] - 1
            conn.execute('UPDATE posts SET reports = ? WHERE id = ?', (new_reports, post_id))
            conn.commit()
        else:
            new_reports = 0 # 通報が0なら、0のまま
        conn.close()
        return jsonify({'reports': new_reports}) # 404エラーではなく、現在の通報数を返す
    return jsonify({'error': 'Post not found'}), 404