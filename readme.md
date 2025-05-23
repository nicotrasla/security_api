# Security API

Este proyecto es una API de seguridad que incluye funcionalidades como escaneo de DNS, consultas WHOIS, escaneo con Nmap y búsquedas de Google Dork. También incluye páginas personalizadas para errores 404 y 500.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Docker Compose](#docker-compose)

---

## Características

- **Google Dork**: Realiza búsquedas avanzadas en Google.
- **Escaneo DNS**: Obtén registros DNS de un dominio.
- **Consultas WHOIS**: Recupera información WHOIS de un dominio.
- **Escaneo Nmap**: Realiza escaneos de puertos en un objetivo.
- **Páginas de error personalizadas**: Incluye páginas personalizadas para errores 404 y 500.

---

## Requisitos

- Python 3.11 o superior
- Django 5.2
- Dependencias adicionales especificadas en `requirements.txt`

---

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/nicotrasla/security_api.git
   cd security_api
   ```

2. Crea y activa un entorno virtual (opcional):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicia el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

---

## Docker Compose

Para ejecutar el proyecto usando Docker Compose:

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Crea un archivo `.env` en el directorio raíz con las siguientes variables:

   ```
   API_URL=http://web:8000/api/analyze/
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Construye y ejecuta los contenedores:

   ```bash
   docker-compose up --build
   ```

4. El servicio estará disponible en:

   - API: http://localhost:8000
   - Los informes generados se guardarán en el directorio `hallazgos/`

5. Para detener los servicios:

   ```bash
   docker-compose down
   ```

---

## Uso

Acceso a la API
El servidor estará disponible en http://127.0.0.1:8000/.
Puedes interactuar con los endpoints utilizando el postman collection en `./JsonCollection `
