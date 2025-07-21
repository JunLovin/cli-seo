# SEO Web Auditor 🔍

Un auditor web CLI que utiliza Gemini AI para analizar páginas web y proporcionar puntuaciones de SEO, Performance, Accessibility y Best Practices similares a las de Google Lighthouse.

## 🪟 Preview

https://github.com/user-attachments/assets/69d87ed2-f094-4715-8118-a198543dd427

## ✨ Características

- **Análisis completo**: Evalúa SEO, Performance, Accessibility y Best Practices
- **Interfaz CLI colorida**: Utiliza códigos ANSI para una mejor visualización
- **Puntuación tipo Lighthouse**: Sistema de puntuación de 0-100 puntos
- **Web scraping automático**: Extrae y analiza el HTML de cualquier URL
- **Recomendaciones específicas**: Proporciona sugerencias accionables para mejorar

## 📋 Requisitos

- Python 3.7+
- API Key de Google Gemini AI

## 🛠️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/seo-web-auditor.git
cd seo-web-auditor
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en el directorio raíz y añade tu API key de Gemini:
```env
GEMINI_KEY=tu_api_key_aqui
```

### Dependencias

Las siguientes librerías son necesarias (incluidas en `requirements.txt`):

```
beautifulsoup4>=4.12.0
google-genai>=0.5.0
python-dotenv>=1.0.0
requests>=2.31.0
```

## 🚀 Uso

Ejecuta el script desde la línea de comandos proporcionando la URL que deseas analizar:

```bash
python main.py https://ejemplo.com
```

### Ejemplo de salida:

```
🔍 Analizando la página 'https://ejemplo.com'...

📊 PUNTUACIÓN GENERAL: 85/100 ⚠️

📈 DETALLE POR CATEGORÍAS:

🎯 SEO: 22/25 ✅
⚡ Performance: 20/25 ⚠️
♿ Accessibility: 23/25 ✅
🛡️ Best Practices: 20/25 ⚠️

💡 RECOMENDACIONES PRINCIPALES:

• 📝 Optimizar meta description (actualmente muy larga)
• 🖼️ Añadir atributos alt a 3 imágenes faltantes
• ⚡ Minimizar archivos CSS y JavaScript externos
• 📱 Verificar responsive design en dispositivos móviles

🚀 PRIORIDAD ALTA:

• Corregir estructura de headings (H1 duplicado encontrado)
• Implementar lazy loading para imágenes
```

## 📊 Sistema de Puntuación

El auditor evalúa cuatro categorías principales, cada una con un peso del 25%:

### 🎯 SEO (25 puntos)
- **Title tag**: Longitud y presencia
- **Meta description**: Optimización y longitud
- **H1 tag**: Unicidad y descriptividad
- **Estructura de headings**: Jerarquía H1>H2>H3
- **Alt en imágenes**: Cobertura y calidad

### ⚡ Performance (25 puntos)
- **Recursos externos**: Cantidad de CSS/JS
- **Optimización de imágenes**: Formato y tamaño
- **Recursos críticos**: CSS inline vs externo
- **Estructura del DOM**: Complejidad y profundidad

### ♿ Accessibility (25 puntos)
- **Alt en imágenes**: Cobertura completa
- **Contraste de colores**: Suficiencia visual
- **Elementos focuseables**: Indicadores de focus
- **Estructura semántica**: Uso correcto de tags

### 🛡️ Best Practices (25 puntos)
- **Validación HTML**: Errores básicos
- **HTTPS**: Protocolo seguro
- **Recursos optimizados**: Dimensiones apropiadas
- **Meta viewport**: Configuración móvil

### Rangos de puntuación:
- **90-100**: ✅ Excelente (Verde)
- **70-89**: ⚠️ Necesita mejoras (Amarillo)
- **0-69**: ❌ Crítico (Rojo)

## ⚠️ Disclaimer Importante

**Este auditor utiliza inteligencia artificial y puede ser inconsistente en sus evaluaciones.** La IA puede cometer errores o proporcionar puntuaciones variables para el mismo contenido. Además, el análisis se basa en el HTML obtenido mediante web scraping con Beautiful Soup, que puede no reflejar completamente la página original renderizada.

**Para análisis profesionales y resultados más precisos, se recomienda utilizar:**
- [Google Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

Este proyecto está pensado como una herramienta experimental y de aprendizaje, no como un reemplazo de herramientas profesionales de auditoría web.

## 📝 Configuración de la API

Para obtener tu API key de Google Gemini:

1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API key
4. Cópiala y pégala en tu archivo `.env`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🐛 Reportar Issues

Si encuentras algún problema o tienes sugerencias, por favor crea un [issue](https://github.com/JunLovin/seo-web-auditor/issues) en GitHub.

## 📞 Soporte

Para preguntas o soporte, puedes:
- Abrir un issue en GitHub
- Contactar al mantenedor del proyecto

---

⚠️ **Recordatorio**: Esta herramienta utiliza IA y sus resultados pueden variar. Para auditorías críticas, utiliza herramientas especializadas como Google Lighthouse.
