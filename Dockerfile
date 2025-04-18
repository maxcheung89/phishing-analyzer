FROM python:3.10-slim

WORKDIR /app

# Install required tools
RUN apt update && apt install -y \
    curl \
    clamav \
    clamav-freshclam \
    tshark \
    iputils-ping \
 && apt clean

# Copy app files
COPY backend/ /app/
COPY analyzer/analyzer.py /app/analyzer.py
COPY secrets/ /app/secrets/
COPY requirements.txt /app/

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
