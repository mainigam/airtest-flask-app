import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
app=Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_api(api_id):
    conn = get_db_connection()
    api = conn.execute('SELECT * FROM apis WHERE id = ?',
                        (api_id,)).fetchone()
    conn.close()
    if api is None:
        abort(404)
    return api

@app.route('/')
def index():
    conn = get_db_connection()
    apis = conn.execute('SELECT * FROM apis').fetchall()
    conn.close()
    return render_template('index.html', apis=apis)

@app.route('/<int:api_id>')
def api(api_id):
    api = get_api(api_id)
    return render_template('post.html', api=api)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO apis (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_api(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE apis SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', api=api)