# ReconBot - Herramienta de Reconocimiento Automatizado

ReconBot es una herramienta de seguridad que realiza análisis automatizados de dominios, incluyendo:

- Resolución de registros DNS
- Consultas WHOIS
- Análisis de visibilidad web mediante Dorking
- Análisis semántico con IA
- Generación de informes en PDF y HTML

## Requisitos Previos

- Python 3.11 o superior
- Cuenta en OpenAI (para el análisis con IA)
- Conexión a Internet

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/nicotrasla/security_api.git
cd reconbot
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar las variables de entorno:
   - Crear un archivo `.env` en el directorio raíz
   - Añadir las siguientes variables:

```env
API_URL=http://localhost:8000/api/analyze/
OPENAI_API_KEY=tu_clave_api_aqui
```

## Obtención de la API Key de OpenAI

1. Crear una cuenta en OpenAI:

   - Visitar [https://platform.openai.com/signup](https://platform.openai.com/signup)
   - Completar el proceso de registro

2. Obtener la API Key:

   - Iniciar sesión en [https://platform.openai.com/](https://platform.openai.com/)
   - Hacer clic en el icono de perfil (esquina superior derecha)
   - Seleccionar "View API keys"
   - Hacer clic en "Create new secret key"
   - Dar un nombre descriptivo a la clave
   - Copiar la clave generada (solo se muestra una vez)
   - Pegar la clave en el archivo `.env` como valor de `OPENAI_API_KEY`

3. Verificar la API Key:

   - La clave debe comenzar con "sk-"
   - Tener cuidado de no compartirla ni subirla a repositorios públicos
   - Si la clave se compromete, se puede revocar y generar una nueva

## Uso

1. Ejecutar el análisis de un dominio:

```bash
python reconbot.py ejemplo.com
```

2. Los resultados se guardarán en el directorio `hallazgos`:
   - `reconbot_ejemplo_com.json` - Datos brutos en formato JSON
   - `reconbot_ejemplo_com_report.pdf` - Informe en PDF
   - `reconbot_ejemplo_com_report.html` - Informe en HTML

## Características

### Análisis DNS

- Registros A
- Registros MX
- Registros NS
- Registros SOA
- Registros TXT

### Información WHOIS

- Registrar
- Fechas de creación y expiración
- Servidores de nombres
- Estado del dominio

### Búsquedas Dork

- Archivos de configuración
- Directorios expuestos
- Archivos de respaldo
- Paneles de administración

### Análisis con IA

- Resumen ejecutivo
- Hallazgos críticos
- Recomendaciones de seguridad
- Enlaces relevantes

## Estructura de Informes

### Informe HTML

- Diseño responsive
- Enlaces clickeables
- Secciones bien organizadas
- Resumen ejecutivo generado por IA
- Fecha y hora del análisis

### Informe PDF

- Diseño profesional
- Secciones claramente diferenciadas
- Resumen ejecutivo
- Hallazgos detallados
- Recomendaciones de seguridad

## Notas de Seguridad

- Usar la herramienta solo en dominios autorizados
- No compartir las API keys
- Mantener las dependencias actualizadas
- Revisar los resultados antes de tomar acciones

## Solución de Problemas

### Error de API Key

- Verificar que la clave esté correctamente copiada
- Asegurar que la clave tenga el formato correcto (sk-...)
- Comprobar que la cuenta de OpenAI esté activa

### Error de Conexión

- Verificar la conexión a Internet
- Comprobar que el dominio sea accesible
- Asegurar que el servidor API esté funcionando

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Hacer fork del repositorio
2. Crear una rama para la característica
3. Hacer commit de los cambios
4. Hacer push a la rama
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
