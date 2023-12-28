FROM python:3.9-slim

RUN useradd -u 3446 airflow-git

WORKDIR /app/

COPY git_scripts /app/

RUN pip install click

USER airflow-git

CMD ["python", "/app/main.py"]