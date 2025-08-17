# Generador de Rostros LoRA

Este repositorio contiene una aplicación web desarrollada con Django que permite generar rostros sintéticos a partir de atributos seleccionados. La generación de imágenes se realiza a través de un servicio externo al que se accede mediante una petición HTTP.

## Requisitos
- Python 3
- Django
- requests
- uvicorn (para ejecutar el servicio de generación)

## Instalación
1. Clona este repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd generador-rostros-lora
   ```
2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración
- Si deseas cambiar la URL del servicio generador de rostros, edita el archivo `generador/views.py` donde se realiza la petición HTTP.
- Asegúrate de tener [ngrok](https://ngrok.com/) instalado para exponer el servicio de generación si es necesario.

## Ejecución
1. Inicia el servicio de generación (FastAPI o similar):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. Expon el servicio con ngrok:
   ```bash
   ./ngrok http 8000
   ```
3. Ejecuta la aplicación Django:
   ```bash
   python manage.py runserver
   ```
4. Abre tu navegador en `http://127.0.0.1:8000/` para acceder a la aplicación.

