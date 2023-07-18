FROM python:3
WORKDIR /srv/app
COPY . .
RUN pip install --no-cache-dir -e .
