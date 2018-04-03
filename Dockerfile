FROM python:3.6

WORKDIR /pip
COPY requirements.txt /pip/requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

WORKDIR /src/pybot

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
