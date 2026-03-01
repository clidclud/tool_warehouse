FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8002

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8002", "--timeout", "120", "--workers", "3"]