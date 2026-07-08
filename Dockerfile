# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalamos dependencias (asumiendo que tienes un archivo requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de tu app
COPY . .

# Exponemos el puerto de Flask
EXPOSE 5000

# Comando para iniciar la aplicación (ajusta según tu archivo principal, ej: app.py)
CMD ["python", "app.py"]
