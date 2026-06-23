FROM python:3.10-slim

LABEL maintainer="GhostTrace"
LABEL description="Stealth Proxy Chain Analyzer"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tor \
    gcc \
    libssl-dev \
    net-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN echo "ControlPort 9051" >> /etc/tor/torrc && \
    echo "SOCKSPort 9050" >> /etc/tor/torrc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p output/logs output/captures output/sessions

RUN cp config/settings.yaml.example config/settings.yaml 2>/dev/null || true

EXPOSE 5000

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]