FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

COPY . .

CMD ["gunicorn", "page_analyzer.app:app", "--bind", "0.0.0.0:8000"]
