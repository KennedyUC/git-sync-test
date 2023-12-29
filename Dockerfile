FROM python:3.9-slim

RUN useradd -u 3446 airflow-git

WORKDIR /app/

RUN apt update && \
    apt install git -y && \
    pip install click

COPY git_scripts /app/

RUN mkdir -p git/dags && \
    chown -R airflow-git /app/

USER airflow-git

CMD ["python", "/app/main.py"]