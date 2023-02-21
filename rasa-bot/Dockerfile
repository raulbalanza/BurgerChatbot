FROM python:3.9.16-buster

COPY requirements.txt /

RUN apt update
RUN apt -y install ffmpeg
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download es_core_news_md
RUN rasa telemetry disable

# Zona horaria
RUN ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime
RUN echo "Europe/Madrid" > /etc/timezone

COPY . /app

WORKDIR /app
RUN rasa train
CMD rasa run --enable-api --cors "*" --debug

