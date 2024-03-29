FROM python:3.9-alpine

# VOLUME .
COPY . /app
WORKDIR /app

EXPOSE 5000

RUN pip install --index-url=https://pypi.python.org/simple/ -r requirements.txt \
    && apt install -y $(cat requirements.apt)

#ENTRYPOINT export FLASK_APP=app.py && flask run --host 0.0.0.0
ENTRYPOINT gunicorn --bind 0.0.0.0:5000 app:app
