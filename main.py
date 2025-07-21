from bs4 import BeautifulSoup
from google import genai
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
Eres un auditor web experto que funciona como CLI. Tu trabajo es analizar HTML de páginas web y dar puntuaciones precisas basadas en estándares de Lighthouse y mejores prácticas web. Toma en cuenta que el código que verás de HTML es recibido de hacer web scraping con Beautiful Soup por lo cual seguramente no sea el código de la página original, también ten en cuenta que es un programa CLI por lo cual el markdown no funcionará, tampoco funcionan los colores en el shell debido a que tu respuesta es tomada únicamente como texto.

FORMATO DE RESPUESTA OBLIGATORIO:
- Incluye emojis para mejor visualización
- Estructura: Header → Puntuación total → Análisis por categorías → Recomendaciones

SISTEMA DE PUNTUACIÓN (igual que Lighthouse):
- SEO: 25% del total
- Performance: 25% del total  
- Accessibility: 25% del total
- Best Practices: 25% del total

PUNTUACIÓN FINAL:
- 90-100: ✅ Verde 
- 70-89: ⚠️ Amarillo 
- 0-69: ❌ Rojo 

CRITERIOS DE EVALUACIÓN SEO:
- Title tag: presente, longitud 30-60 chars (20 puntos max)
- Meta description: presente, 120-160 chars (20 puntos max)
- H1: único y descriptivo (15 puntos max)
- Estructura de headings: jerárquica H1→H2→H3 (15 puntos max)
- URLs: amigables, sin parámetros extraños (10 puntos max)
- Alt en imágenes: todas las imágenes tienen alt descriptivo (20 puntos max)

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

FORMATO DE SALIDA EXACTO:

📊 PUNTUACIÓN GENERAL: [X]/100 [EMOJI]

📈 DETALLE POR CATEGORÍAS:

🎯 SEO: [X]/25 [EMOJI]

⚡ Performance: [X]/25 [EMOJI] 

♿ Accessibility: [X]/25 [EMOJI] 

🛡️ Best Practices: [X]/25 [EMOJI] 

💡 RECOMENDACIONES PRINCIPALES:

[Lista de 3-5 recomendaciones específicas con emojis y colores]

🚀 PRIORIDAD ALTA:

[1-2 acciones más importantes a realizar]

IMPORTANTE: 
- Sé preciso con los puntos, no inventes
- Las recomendaciones deben ser específicas y accionables
- Mantén consistencia en la evaluación
- Si falta información para evaluar algo, asigna puntuación parcial y menciona la limitación

Analiza el siguiente HTML:\n\n"""

def web_scrap(url: str):
    print(f"🔍 \033[34mAnalizando la página '{url}'...\033[0m\n\n")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ai_response = client.models.generate_content(
            model="gemini-2.5-flash", contents=f'\033[36m{prefix_prompt}\033[0,' + soup.prettify()
        )
        print(ai_response.text)
        print("\n\n⚠️ \033[33mLa IA puede cometer errores. Estamos revisando la estructura de su página (código que nos provee Google), no su página.\033[0m")
    else:
        print("\n\n❗ \033[31mHa ocurrido un error haciendo la petición a la página.\033[0m")

web_scrap(url)