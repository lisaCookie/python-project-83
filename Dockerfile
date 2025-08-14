FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

CMD ["gunicorn", "page_analyzer.app:app", "--bind", "0.0.0.0:8000"]