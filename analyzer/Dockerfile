FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    curl clamav clamav-freshclam tshark iputils-ping && \
    mkdir -p /app/results && apt clean

WORKDIR /app
COPY analyzer.py .

CMD ["python3", "analyzer.py"]
