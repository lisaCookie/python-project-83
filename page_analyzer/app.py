import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from .parser import parse_url
from .utils import normalize_url, validate_url
from .work_with_db import (
    get_all_urls,
    get_checks_by_url_id,
    get_url_by_id,
    insert_check,
    insert_url,
)

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/', methods=['GET'], endpoint='home')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'], endpoint='urls')
def all_urls():
    if request.method == 'POST':
        url_input = request.form.get('url')
        error = validate_url(url_input)
        if error:
            flash(error, 'danger')
            return redirect(url_for('home'))
        
        base_url = normalize_url(url_input)
        new_id, is_new = insert_url(base_url)
        
        if not is_new:
            flash('Страница уже существует', 'info')
        else:
            flash('Страница успешно добавлена', 'success')
        
        return redirect(url_for('url_detail', id=new_id))
    
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_detail(id):
    url_record = get_url_by_id(id)
    if not url_record:
        flash('URL не найден', 'warning')
        return redirect(url_for('urls'))
    
    checks = get_checks_by_url_id(id)
    return render_template('url.html', url=url_record, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    url_record = get_url_by_id(id)
    if not url_record:
        flash('URL не найден', 'warning')
        return redirect(url_for('urls'))
    
    url = url_record['name']
    status_code, h1, title, description = parse_url(url)
    
    insert_check(id, status_code or 500, h1, title, description)
    
    if status_code is None or status_code >= 400:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Страница успешно проверена', 'success')
    
    return redirect(url_for('url_detail', id=id))


if __name__ == '__main__':
    app.run(debug=True)
