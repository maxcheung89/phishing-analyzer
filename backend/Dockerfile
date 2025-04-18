FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install -y python3-pip && \
    pip install --no-cache-dir flask requests cryptography

EXPOSE 5000

CMD ["python", "app.py"]
