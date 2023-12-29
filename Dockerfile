FROM python:3.9-slim

RUN useradd -u 3446 airflow-git

RUN apt update && \
    apt install git -y

WORKDIR /app/

COPY git_scripts /app/

RUN pip install click

RUN chown -R airflow-git /app/

RUN mkdir -p /opt/airflow/dag && \
    chown -R 3446:3446 /opt/airflow/dag && \
    chmod -R u+w /opt/airflow/dag

USER airflow-git

CMD ["python", "/app/main.py"]