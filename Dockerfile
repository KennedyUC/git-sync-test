FROM python:3.9-slim

RUN useradd -u 3446 airflow-git

RUN apt update && \
    apt install git -y

WORKDIR /app/

COPY git_scripts /app/

RUN pip install click

RUN chown -R airflow-git /app/

USER airflow-git

CMD ["python", "/app/main.py"]