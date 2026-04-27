# 📸 Instagram Scraper

## 📝 Descripción General

Este proyecto implementa un proceso de **web scraping sobre perfiles públicos de Instagram**, sin utilizar la API oficial.

El objetivo es comprender cómo funciona la carga de datos en aplicaciones modernas basadas en JavaScript, analizando las solicitudes web, el uso de cookies y la estructura dinámica del contenido.

El scraper permite extraer:

* Información del perfil
* Publicaciones recientes
* Metadatos (likes, fechas, descripciones)
* Hashtags y menciones

---

## 🎯 Objetivo Académico

Desarrollar un scraper que:

* Analice el funcionamiento de las solicitudes web
* Extraiga información de una página pública
* Implemente estrategias para evitar bloqueos
* Documente el proceso y los desafíos encontrados

---

## ⚙️ Tecnologías Utilizadas

* Python 3.8+
* Playwright
* Requests
* JSON

---

## ⚠️ Justificación del Uso de Playwright

Aunque el enunciado restringe el uso de herramientas como Selenium o BeautifulSoup, en este proyecto se utiliza **Playwright únicamente como herramienta de apoyo** para:

* Analizar el comportamiento dinámico de Instagram
* Capturar cookies de sesión necesarias
* Comprender las solicitudes internas del navegador

⚠️ **Importante:**
La lógica del scraping no depende de una API oficial, sino del análisis de:

* Estructura HTML
* Selectores CSS
* Comportamiento del cliente web

---

## 🔍 Análisis de Solicitudes Web

Durante el desarrollo se identificó que Instagram:

* Carga contenido dinámicamente mediante JavaScript
* Requiere cookies de sesión válidas (`sessionid`, `csrftoken`)
* Utiliza endpoints internos protegidos

Ejemplo de elementos clave:

* Headers necesarios:

  * User-Agent realista
  * Cookies activas
* Contenido cargado tras scroll (lazy loading)

Esto implica que:

* No es posible obtener datos completos con requests simples sin autenticación
* Se requiere simular una sesión válida

---

## 🛡️ Estrategias para Evitar Bloqueos

Se implementaron varias técnicas:

* ⏱️ Delays entre peticiones (2–5 segundos)
* 🍪 Uso de cookies persistentes
* 🧍 Simulación de comportamiento humano (scroll progresivo)
* 🧠 User-Agent realista
* 🔁 Reutilización de sesión

---

## 🧠 Desafíos Encontrados

### 1. Contenido dinámico

Instagram no entrega HTML completo inicialmente.

**Solución:**

* Uso de renderizado con navegador controlado
* Esperas explícitas (`wait_for_timeout`)

---

### 2. Bloqueos HTTP (403 / 429)

Intentos directos de descarga de imágenes fallaban.

**Solución:**

* Uso de cookies activas en las peticiones
* Descarga mediante contexto autenticado

---

### 3. Cambios en el DOM

Los selectores CSS cambian frecuentemente.

**Solución:**

* Uso de múltiples selectores alternativos
* Manejo de errores con `try/except`

---

### 4. Limitaciones de acceso

Algunas funcionalidades requieren interacción adicional.

**Solución:**

* Limitar el scraping a cuentas públicas
* Reducir número de peticiones

---

## 📂 Estructura del Proyecto

```
instagram_scraper/
├── data/
│   ├── instagram_cookies.json
│   └── resultados/
│       └── perfil_extraido.json
├── scraper/
│   ├── browser.py
│   ├── profile.py
│   ├── posts.py
│   ├── display.py
├── web_dashboard/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── server.py
├── downloads/
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Instalación

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## ▶️ Ejecución

```bash
python main.py
```

### Primer uso:

1. Se abrirá el navegador
2. Inicia sesión manualmente
3. Presiona ENTER en la consola

---

## 📊 Salida del Sistema

Los datos se guardan en:

```
data/resultados/perfil_extraido.json
```

Ejemplo:

```json
{
  "perfil": {
    "username": "nasa",
    "followers_count": "89.5M"
  },
  "publicaciones": [...]
}
```

---

## 🖥️ Dashboard Web

```bash
cd web_dashboard
python server.py
```

Abrir en navegador:

```
http://localhost:8000
```

---
## 🔐 Seguridad

⚠️ Importante:
El archivo `data/instagram_cookies.json` NO se incluye en el repositorio por razones de seguridad.

Este archivo contiene cookies de sesión que permiten autenticación en Instagram.

Para ejecutar el proyecto:
1. Ejecuta el scraper
2. Inicia sesión manualmente
3. Las cookies se generarán automáticamente

## 🔒 Consideraciones Éticas

* Solo se analizan perfiles públicos
* No se utiliza la API oficial
* No se realiza uso comercial de los datos
* Se respetan límites para evitar sobrecarga del servidor

---

## ⚠️ Limitaciones

* No garantiza estabilidad (Instagram cambia constantemente)
* Algunas imágenes pueden no descargarse
* No se extraen todos los comentarios
* Dependencia de cookies válidas

---

## 🎯 Conclusión

Este proyecto demuestra la comprensión de:

* Cómo funcionan las aplicaciones web modernas
* El uso de cookies y sesiones
* Técnicas de scraping en entornos dinámicos
* Estrategias para evitar bloqueos

---

## 📄 Licencia

Proyecto con fines educativos.
