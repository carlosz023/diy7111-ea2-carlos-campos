
# Monitoreo de Infraestructura - Caso HealthTrack

Este proyecto despliega un servidor de Prometheus containerizado para la startup HealthTrack, implementando persistencia dual (volúmenes para datos y montajes fijos para configuración).

## Variables de Entorno
* `TZ`: America/Santiago
* `APP_ENV`: production

## Requisitos de Almacenamiento
* **Bind Mount:** Modifica `./config/prometheus.yml` directamente desde el host.
* **Named Volume:** Los datos persisten en el volumen `prometheus_data`.

## Comandos para Despliegue Local
```powershell
# Construir e iniciar el contenedor en segundo plano
docker compose up -d --build

# Verificar estado
docker compose ps
