FROM python:3
WORKDIR /srv/app
COPY . .
RUN pip install --no-cache-dir --editable .
RUN pip install gunicorn==21.1.0
