FROM prom/prometheus:latest
LABEL maintainer='Carlos Campos'
COPY config/prometheus.yml /etc/prometheus/prometheus.yml
EXPOSE 9090