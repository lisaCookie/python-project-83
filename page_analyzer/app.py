# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import validators
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY 

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/', methods=['GET', 'POST'], endpoint='home')
def index():
    if request.method == 'POST':
        url_input = request.form.get('url')
        # Валидация URL
        if not url_input:
            flash('Пожалуйста, введите URL', 'error')
            return render_template('index.html')
        if len(url_input) > 255:
            flash('URL не должен превышать 255 символов', 'error')
            return render_template('index.html')
        if not validators.url(url_input):
            flash('Некорректный URL', 'error')
            return render_template('index.html')

        # Проверка, что сайт с таким именем еще не добавлен
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM urls WHERE name = %s", (url_input,))
                existing = cursor.fetchone()
                if existing:
                    flash('Этот URL уже добавлен', 'info')
                    return redirect(url_for('url_detail', id=existing[0]))
                # Добавляем новый URL
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                    (url_input,)
                )
                new_id = cursor.fetchone()[0]
        flash('URL успешно добавлен', 'success')
        return redirect(url_for('url_detail', id=new_id))
    return render_template('index.html')

@app.route('/urls', endpoint='urls')
def all_urls():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, created_at FROM urls ORDER BY created_at DESC")
            urls = cursor.fetchall()
    return render_template('urls.html', urls=urls)

@app.route('/urls/<int:id>')
def url_detail(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (id,))
            url_record = cursor.fetchone()
    if url_record:
        return render_template('url_detail.html', url=url_record)
    else:
        flash('URL не найден', 'warning')
        return redirect(url_for('urls'))

