
import os

import psycopg2
import requests
import validators
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

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
            return render_template('index.html', 
                                   error='Пожалуйста, введите URL')
        if len(url_input) > 255:
            return render_template('index.html', 
                                   error='URL не должен превышать 255 символов')
        if not validators.url(url_input):
            return render_template('index.html', error='Некорректный URL')

        # Проверка, что сайт с таким именем еще не добавлен
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM urls WHERE name = %s", 
                    (url_input,)
                )
                existing = cursor.fetchone()
                if existing:
                    flash('Этот URL уже добавлен', 'info')
                    return redirect(url_for('url_detail', id=existing[0]))
                # Добавить новый URL
                cursor.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                    (url_input,)
                )
                new_id = cursor.fetchone()[0]
        flash('URL успешно добавлен', 'success')
        return redirect(url_for('url_detail', id=new_id))
    return render_template('index.html', error=request.args.get('error'))


@app.route('/urls', methods=['GET', 'POST'], endpoint='urls')
def all_urls():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name, u.created_at, 
                    uc.created_at AS last_check_date, 
                    uc.status_code
                FROM urls u
                LEFT JOIN LATERAL (
                    SELECT created_at, status_code
                    FROM url_checks
                    WHERE url_id = u.id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) uc ON true
                ORDER BY u.created_at DESC
                """)

            urls = cursor.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_detail(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, created_at FROM urls WHERE id = %s", 
                (id,)
            )

            url_record = cursor.fetchone()
            cursor.execute(
                "SELECT id, created_at, status_code" 
                "FROM url_checks " 
                "WHERE url_id = %s " 
                "ORDER BY created_at DESC",
                (id,)
            )
            checks = cursor.fetchall()
    if url_record:
        return render_template(
            'url.html',
            url=url_record[1],
            created_at=url_record[2],
            url_id=url_record[0],
            checks=checks
        )
    else:
        flash('URL не найден', 'warning')
        return redirect(url_for('urls'))


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE id = %s", (id,))
            url_record = cursor.fetchone()
            if not url_record:
                flash('URL not found', 'warning')
                return redirect(url_for('urls'))
            url = url_record[0]
            
            try:
                response = requests.get(url, timeout=10)
                status_code = response.status_code
                
                if status_code < 400:
                    cursor.execute(
                        "INSERT INTO url_checks (url_id, status_code) " 
                        "VALUES (%s, %s)",
                        (id, status_code)
                    )
                    flash('Проверка успешно добавлена', 'success')
                else:
                    flash('Произошла ошибка при проверке', 'danger')
            except requests.RequestException:
                flash('Произошла ошибка при проверке', 'danger')
    
    return redirect(url_for('url_detail', id=id))

