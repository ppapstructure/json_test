FROM python:3.8-slim

WORKDIR /app

COPY ./project /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]