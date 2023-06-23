FROM python:3.11-slim-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./sinka97 ./

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]