FROM python:3.10-slim-bullseye

RUN pip3 install trino dash pandas

WORKDIR /app
ENTRYPOINT [ "python3", "app.py" ]