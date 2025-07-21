from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import os
import argparse 

parser = argparse.ArgumentParser(description="Web Scraping para que Gemini revise el SEO de una URL dada.")
parser.add_argument('url', type=str, help="La URL del sitio que quieres que Gemini revise.")
args = parser.parse_args()
url = args.url

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')

client = genai.Client(api_key=GEMINI_KEY)

prefix_prompt = """
Eres un auditor web experto que funciona como CLI. DEBES SER EXTREMADAMENTE CONSISTENTE en tus puntuaciones. Tu trabajo es analizar HTML de páginas web y dar puntuaciones precisas basadas en estándares de Lighthouse y mejores prácticas web. Toma en cuenta que el código que verás de HTML es recibido de hacer web scraping con Beautiful Soup por lo cual seguramente no sea el código de la página original, también ten en cuenta que es un programa CLI por lo cual el markdown no funcionará.

⚠️ REGLAS DE CONSISTENCIA OBLIGATORIAS:
- Usa EXACTAMENTE los mismos criterios cada vez
- NO uses palabras como "aproximadamente" o "cerca de" 
- Si una página tiene las mismas características, DEBE recibir la misma puntuación
- Variación máxima permitida: ±2 puntos para la misma página


FORMATO DE RESPUESTA OBLIGATORIO:
- Usa códigos ANSI para colores (\033[32m para verde, \033[33m para amarillo, \033[31m para rojo, \033[0m para reset)
- Incluye emojis para mejor visualización
- Estructura: Header → Puntuación total → Análisis por categorías → Recomendaciones

SISTEMA DE PUNTUACIÓN (igual que Lighthouse):
- SEO: 25% del total
- Performance: 25% del total  
- Accessibility: 25% del total
- Best Practices: 25% del total

PUNTUACIÓN FINAL:
- 90-100: ✅ Verde (\033[32m) - Excelente
- 70-89: ⚠️ Amarillo (\033[33m) - Necesita mejoras
- 0-69: ❌ Rojo (\033[31m) - Crítico

SEO (25 puntos total):
✅ Title tag: 
   - 30-60 caracteres = 5 puntos
   - 20-29 o 61-70 caracteres = 3 puntos
   - <20 o >70 caracteres = 1 punto
   - Ausente = 0 puntos

✅ Meta description:
   - 120-160 caracteres = 5 puntos
   - 80-119 o 161-200 caracteres = 3 puntos
   - <80 o >200 caracteres = 1 punto
   - Ausente = 0 puntos

✅ H1 tag:
   - 1 H1 presente y descriptivo = 5 puntos
   - 1 H1 presente pero genérico = 3 puntos
   - Más de 1 H1 o muy corto = 1 punto
   - Sin H1 = 0 puntos

✅ Estructura headings:
   - Jerarquía perfecta H1>H2>H3 = 5 puntos
   - Jerarquía con 1-2 errores menores = 3 puntos
   - Jerarquía rota o caótica = 1 punto
   - Sin estructura = 0 puntos

✅ Alt en imágenes:
   - 100% de imágenes con alt descriptivo = 5 puntos
   - 80-99% con alt = 3 puntos
   - 50-79% con alt = 2 puntos
   - <50% con alt = 1 punto
   - Sin alt o sin imágenes = 0 puntos

CRITERIOS ACCESSIBILITY:
- Alt en imágenes: 100% = 25 puntos, 80-99% = 20 puntos, <80% = 10 puntos
- Contraste de colores: evalúa si hay suficiente contraste (25 puntos max)
- Elementos focuseables: links y botones tienen indicadores de focus (25 puntos max)
- Estructura semántica: uso correcto de tags semánticos (25 puntos max)

CRITERIOS BEST PRACTICES:
- Errores de HTML: validación básica (25 puntos max)
- HTTPS: detectar si usa protocolo seguro (25 puntos max)
- Recursos optimizados: imágenes sin dimensiones excesivas (25 puntos max)
- Meta viewport: presente y configurado (25 puntos max)

PERFORMANCE (evalúa según HTML):
- Cantidad de recursos: CSS/JS externos (25 puntos max)
- Imágenes optimizadas: formato y tamaño apropiados (25 puntos max)
- Recursos críticos: CSS inline vs externo (25 puntos max)
- Estructura del DOM: profundidad y complejidad (25 puntos max)

🚨 IMPORTANTE: Cuenta EXACTAMENTE y aplica estos valores. NO improvises puntuaciones.

FORMATO DE SALIDA EXACTO:

📊 \\033[45mPUNTUACIÓN GENERAL: [X]/100\\033[0m [EMOJI]

📈 \\033[36mDETALLE POR CATEGORÍAS: \\033[0m

🎯 \\033[36mSEO: [X]/25 [EMOJI] \\033[0m

⚡ \\033[36mPerformance: [X]/25 [EMOJI] \\033[0m

♿ \\033[36mAccessibility: [X]/25 [EMOJI] \\033[0m

🛡️ \\033[36mBest Practices: [X]/25 [EMOJI] \\033[0m

💡 \\033[36mRECOMENDACIONES PRINCIPALES:\\033[0m

[Lista de 3-5 recomendaciones específicas con emojis y colores]

🚀 \\033[36mPRIORIDAD ALTA: \\033[0m

[1-2 acciones más importantes a realizar]

EJEMPLOS DE PUNTUACIÓN EXACTA:
- Title 30-60 chars = 20 puntos
- Title 20-29 o 61-70 chars = 15 puntos  
- Title <20 o >70 chars = 5 puntos
- Sin title = 0 puntos

NO uses rangos como "aproximadamente" o "cerca de". Usa EXACTAMENTE estos valores.

IMPORTANTE: 
- Sé preciso con los puntos, no inventes
- Las recomendaciones deben ser específicas y accionables
- Mantén consistencia en la evaluación
- Si falta información para evaluar algo, asigna puntuación parcial y menciona la limitación

IMPORTANTE: Mantén consistencia. Si una página tiene las mismas características técnicas, debe recibir la misma puntuación ±2 puntos máximo.

Analiza el siguiente HTML:\n\n"""

def replace_ansi(text: str):
    text = text.replace('\\033', '\033')
    return text

def web_scrap(url: str):
    print(f"🔍 \033[34mAnalizando la página '{url}'...\033[0m\n\n")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ai_response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prefix_prompt + soup.prettify(),
            config=types.GenerateContentConfig(temperature=0.1, top_p=0.8, top_k=10),
        )
        processed_response = replace_ansi(ai_response.text)
        print(processed_response)
        print("\n\n⚠️ \033[33mLa IA puede cometer errores. Estamos revisando la estructura de su página (código que nos provee Google), no su página.\033[0m")
    else:
        print("\n\n❗ \033[31mHa ocurrido un error haciendo la petición a la página.\033[0m")

web_scrap(url)