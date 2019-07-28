FROM python:3

RUN pip install pagr
ADD app /app

CMD ["python", "-m", "pagr.runner", "/app"]
