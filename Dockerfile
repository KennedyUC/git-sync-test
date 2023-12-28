FROM python:3.9-slim

RUN apt update && \
    apt install git -y

WORKDIR /app/

COPY git_scripts /app/

RUN pip install click

USER root

CMD ["python", "/app/main.py"]