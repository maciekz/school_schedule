FROM python:3
WORKDIR /srv/app
COPY . .
RUN pip install -r requirements.txt
