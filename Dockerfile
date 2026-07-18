FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs /app/media /app/assets
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "hospital.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
