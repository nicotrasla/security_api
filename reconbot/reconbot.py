#!/usr/bin/env python3
import dns.resolver
import whois
import requests
from bs4 import BeautifulSoup
from googlesearch import search as google_search
import json
import argparse
from typing import Dict, List, Any
import os
from dotenv import load_dotenv
import openai
from fpdf import FPDF
from datetime import datetime
import html
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ReconBot:
    def __init__(self, domain: str):
        self.domain = domain
        self.results = {
            "dns_records": {},
            "whois_info": {},
            "dork_results": {},
            "ai_analysis": {}
        }
        load_dotenv()
        self.api_url = os.getenv(
            "API_URL", "http://localhost:8000/api/analyze/")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en el archivo .env")

        # Crear directorio de hallazgos si no existe
        self.hallazgos_dir = "hallazgos"
        if not os.path.exists(self.hallazgos_dir):
            os.makedirs(self.hallazgos_dir)

    def get_dns_records(self) -> Dict[str, Any]:
        """Obtiene registros DNS del dominio."""
        try:
            # Registro A
            a_records = dns.resolver.resolve(self.domain, 'A')
            self.results["dns_records"]["A"] = [str(r) for r in a_records]

            # Registro MX
            mx_records = dns.resolver.resolve(self.domain, 'MX')
            self.results["dns_records"]["MX"] = [str(r) for r in mx_records]

            # Registro NS
            ns_records = dns.resolver.resolve(self.domain, 'NS')
            self.results["dns_records"]["NS"] = [str(r) for r in ns_records]

            # Registro SOA
            soa_records = dns.resolver.resolve(self.domain, 'SOA')
            self.results["dns_records"]["SOA"] = [str(r) for r in soa_records]

            # Registro TXT
            try:
                txt_records = dns.resolver.resolve(self.domain, 'TXT')
                self.results["dns_records"]["TXT"] = [
                    str(r) for r in txt_records]
            except:
                self.results["dns_records"]["TXT"] = []

        except Exception as e:
            print(f"Error al obtener registros DNS: {str(e)}")

        return self.results["dns_records"]

    def get_whois_info(self) -> Dict[str, Any]:
        """Obtiene información WHOIS del dominio."""
        try:
            w = whois.whois(self.domain)
            self.results["whois_info"] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status
            }
        except Exception as e:
            print(f"Error al obtener información WHOIS: {str(e)}")

        return self.results["whois_info"]

    def perform_dorking(self) -> Dict[str, List[str]]:
        """Realiza búsquedas Dork sobre el dominio usando DuckDuckGo."""
        dorks = [
            f"site:{self.domain} filetype:env OR filetype:xml OR filetype:conf",
            f"site:{self.domain} (index of OR backup OR admin)"
        ]

        for dork in dorks:
            try:
                print(f"\n[*] Ejecutando búsqueda: {dork}")
                results = []

                # Usar DuckDuckGo para las búsquedas
                import requests
                from bs4 import BeautifulSoup

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

                # Realizar la búsqueda en DuckDuckGo
                search_url = f"https://html.duckduckgo.com/html/?q={dork}"
                response = requests.get(search_url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Buscar enlaces en los resultados
                    for result in soup.find_all('a', class_='result__url'):
                        url = result.get('href')
                        if url and url.startswith('http'):
                            results.append(url)
                            if len(results) >= 5:  # Limitar a 5 resultados
                                break

                self.results["dork_results"][dork] = results
                print(f"[+] Encontrados {len(results)} resultados")

            except Exception as e:
                print(f"Error en búsqueda Dork '{dork}': {str(e)}")
                self.results["dork_results"][dork] = []

        return self.results["dork_results"]

    def analyze_with_ai(self) -> Dict[str, Any]:
        """Envía los resultados a la API de análisis con IA."""
        try:
            response = requests.post(
                self.api_url,
                json={"text": json.dumps(self.results["dork_results"])}
            )
            if response.status_code == 200:
                self.results["ai_analysis"] = response.json()
            else:
                print(f"Error en la API de IA: {response.status_code}")
        except Exception as e:
            print(f"Error al analizar con IA: {str(e)}")

        return self.results["ai_analysis"]

    def generate_ai_summary(self) -> str:
        """Genera un resumen de los hallazgos usando OpenAI."""
        try:
            prompt = f"""
            Analiza los siguientes hallazgos de seguridad para el dominio {self.domain} y genera un informe detallado:

            Registros DNS:
            {json.dumps(self.results['dns_records'], indent=2)}

            Información WHOIS:
            {json.dumps(self.results['whois_info'], indent=2)}

            Resultados de búsquedas Dork:
            {json.dumps(self.results['dork_results'], indent=2)}

            Análisis de IA:
            {json.dumps(self.results['ai_analysis'], indent=2)}

            Por favor, genera un informe que incluya:
            1. Resumen ejecutivo
            2. Hallazgos críticos
            3. Recomendaciones de seguridad
            4. Enlaces relevantes
            5. Conclusión

            El informe debe ser técnico pero comprensible, y enfocarse en los aspectos de seguridad más importantes.
            """

            # Configurar el cliente de OpenAI
            openai.api_key = os.getenv("OPENAI_API_KEY")

            # Intentar generar el resumen con un máximo de 3 intentos
            for attempt in range(3):
                try:
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Eres un experto en seguridad informática que genera informes detallados de análisis de seguridad."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    if attempt < 2:  # Si no es el último intento
                        print(
                            f"Intento {attempt + 1} fallido, reintentando...")
                        import time
                        time.sleep(2)  # Esperar 2 segundos entre intentos
                    else:
                        raise e

        except Exception as e:
            print(f"Error al generar resumen con OpenAI: {str(e)}")
            return "Error al generar el resumen con OpenAI."

    def generate_html_report(self, ai_summary: str):
        """Genera un informe HTML con los resultados."""
        try:
            # Crear el contenido HTML usando variables separadas
            domain = self.domain
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            escaped_summary = html.escape(ai_summary).replace('\n', '<br>')
            dns_html = self._generate_dns_html()
            whois_html = self._generate_whois_html()
            dork_html = self._generate_dork_html()

            html_content = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Informe de Seguridad - {domain}</title>
                <style>
                    :root {{
                        --primary-color: #2c3e50;
                        --secondary-color: #3498db;
                        --accent-color: #e74c3c;
                        --background-color: #f8f9fa;
                        --text-color: #2c3e50;
                        --border-radius: 8px;
                        --box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}

                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        color: var(--text-color);
                        background-color: var(--background-color);
                    }}

                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                    }}

                    .header {{
                        text-align: center;
                        margin-bottom: 40px;
                        padding: 30px;
                        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                        color: white;
                        border-radius: var(--border-radius);
                        box-shadow: var(--box-shadow);
                    }}

                    .header h1 {{
                        margin: 0;
                        font-size: 2.5em;
                        font-weight: 600;
                    }}

                    .header h2 {{
                        margin: 10px 0;
                        font-size: 1.8em;
                        font-weight: 400;
                    }}

                    .timestamp {{
                        font-style: italic;
                        color: rgba(255, 255, 255, 0.9);
                        margin-top: 10px;
                    }}

                    .section {{
                        margin-bottom: 40px;
                        padding: 25px;
                        background-color: white;
                        border-radius: var(--border-radius);
                        box-shadow: var(--box-shadow);
                    }}

                    .section h2 {{
                        color: var(--primary-color);
                        border-bottom: 2px solid var(--secondary-color);
                        padding-bottom: 10px;
                        margin-top: 0;
                    }}

                    .summary {{
                        white-space: pre-wrap;
                        background-color: var(--background-color);
                        padding: 20px;
                        border-radius: var(--border-radius);
                        border-left: 4px solid var(--secondary-color);
                    }}

                    .dns-record, .whois-info {{
                        margin-bottom: 15px;
                        padding: 15px;
                        background-color: var(--background-color);
                        border-radius: var(--border-radius);
                    }}

                    .dns-record h3, .whois-info h3 {{
                        color: var(--secondary-color);
                        margin-top: 0;
                    }}

                    .dork-result {{
                        margin-bottom: 20px;
                        padding: 15px;
                        background-color: var(--background-color);
                        border-radius: var(--border-radius);
                    }}

                    .dork-result h3 {{
                        color: var(--secondary-color);
                        margin-top: 0;
                    }}

                    .url {{
                        color: var(--secondary-color);
                        text-decoration: none;
                        transition: color 0.3s ease;
                    }}

                    .url:hover {{
                        color: var(--accent-color);
                        text-decoration: underline;
                    }}

                    .critical {{
                        color: var(--accent-color);
                        font-weight: bold;
                    }}

                    .recommendation {{
                        background-color: #e8f4f8;
                        padding: 15px;
                        border-radius: var(--border-radius);
                        margin: 10px 0;
                        border-left: 4px solid var(--secondary-color);
                    }}

                    @media print {{
                        body {{
                            background-color: white;
                        }}
                        .section {{
                            box-shadow: none;
                            border: 1px solid #ddd;
                        }}
                        .header {{
                            background: var(--primary-color);
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Informe de Seguridad</h1>
                        <h2>Dominio: {domain}</h2>
                        <p class="timestamp">Fecha: {timestamp}</p>
                    </div>

                    <div class="section">
                        <h2>Resumen del Análisis</h2>
                        <div class="summary">
                            {escaped_summary}
                        </div>
                    </div>

                    <div class="section">
                        <h2>Registros DNS</h2>
                        {dns_html}
                    </div>

                    <div class="section">
                        <h2>Información WHOIS</h2>
                        {whois_html}
                    </div>

                    <div class="section">
                        <h2>Resultados de Búsquedas Dork</h2>
                        {dork_html}
                    </div>
                </div>
            </body>
            </html>
            """

            output_file = os.path.join(
                self.hallazgos_dir, f"reconbot_{self.domain.replace('.', '_')}_report.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n[+] Informe HTML generado: {output_file}")

        except Exception as e:
            print(f"Error al generar el informe HTML: {str(e)}")

    def _generate_dns_html(self) -> str:
        """Genera el HTML para la sección de DNS."""
        html = ""
        for record_type, records in self.results['dns_records'].items():
            html += f'<div class="dns-record">'
            html += f'<h3>{record_type}</h3>'
            for record in records:
                html += f'<p>  - {record}</p>'
            html += '</div>'
        return html

    def _generate_whois_html(self) -> str:
        """Genera el HTML para la sección de WHOIS."""
        html = ""
        for key, value in self.results['whois_info'].items():
            html += f'<div class="whois-info">'
            if isinstance(value, list):
                html += f'<h3>{key}</h3>'
                for item in value:
                    html += f'<p>  - {item}</p>'
            else:
                html += f'<p><strong>{key}:</strong> {value}</p>'
            html += '</div>'
        return html

    def _generate_dork_html(self) -> str:
        """Genera el HTML para la sección de Dork."""
        html = ""
        for dork, urls in self.results['dork_results'].items():
            html += f'<div class="dork-result">'
            html += f'<h3>Búsqueda: {dork}</h3>'
            for url in urls:
                html += f'<p><a href="{url}" class="url" target="_blank">{url}</a></p>'
            html += '</div>'
        return html

    def generate_pdf_report(self, ai_summary: str):
        """Genera un informe PDF con los resultados."""
        try:
            pdf = FPDF()
            pdf.add_page()

            # Configurar fuentes
            try:
                # Nueva forma de agregar fuentes en FPDF2
                pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')
                pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf')
                pdf.add_font('DejaVu', 'I', 'DejaVuSansCondensed-Oblique.ttf')
                font_family = 'DejaVu'
            except:
                font_family = 'helvetica'

            # Configurar colores
            primary_color = (44, 62, 80)    # Azul oscuro
            secondary_color = (52, 152, 219)  # Azul
            accent_color = (231, 76, 60)     # Rojo
            text_color = (44, 62, 80)        # Texto principal
            light_bg = (248, 249, 250)       # Fondo claro

            # Título con fondo
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font(font_family, 'B', 24)
            pdf.cell(0, 30, f'Informe de Seguridad - {self.domain}',
                     new_x="LMARGIN", new_y="NEXT", align='C', fill=True)
            pdf.ln(10)

            # Fecha con estilo
            pdf.set_text_color(*secondary_color)
            pdf.set_font(font_family, 'I', 12)
            pdf.cell(
                0, 10, f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', new_x="LMARGIN", new_y="NEXT")
            pdf.ln(10)

            # Resumen de IA con fondo
            pdf.set_fill_color(*light_bg)
            pdf.set_text_color(*text_color)
            pdf.set_font(font_family, 'B', 16)
            pdf.cell(0, 15, 'Resumen del Análisis',
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            # Fondo para el resumen
            pdf.set_fill_color(*light_bg)
            pdf.rect(10, pdf.get_y(), 190, 60, style='F')

            pdf.set_font(font_family, '', 12)
            pdf.set_text_color(0, 0, 0)
            for line in ai_summary.split('\n'):
                pdf.multi_cell(0, 10, line)
                pdf.ln(2)

            # Registros DNS
            pdf.add_page()
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font(font_family, 'B', 16)
            pdf.cell(0, 15, 'Registros DNS', new_x="LMARGIN",
                     new_y="NEXT", fill=True)
            pdf.ln(5)

            pdf.set_font(font_family, '', 12)
            for record_type, records in self.results['dns_records'].items():
                pdf.set_text_color(*secondary_color)
                pdf.cell(0, 10, f'{record_type}:',
                         new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(0, 0, 0)
                for record in records:
                    pdf.cell(0, 10, f'  - {record}',
                             new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

            # Información WHOIS
            pdf.add_page()
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font(font_family, 'B', 16)
            pdf.cell(0, 15, 'Información WHOIS',
                     new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.ln(5)

            pdf.set_font(font_family, '', 12)
            for key, value in self.results['whois_info'].items():
                pdf.set_text_color(*secondary_color)
                if isinstance(value, list):
                    pdf.cell(0, 10, f'{key}:', new_x="LMARGIN", new_y="NEXT")
                    pdf.set_text_color(0, 0, 0)
                    for item in value:
                        pdf.cell(0, 10, f'  - {item}',
                                 new_x="LMARGIN", new_y="NEXT")
                else:
                    pdf.cell(0, 10, f'{key}: {value}',
                             new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

            # Resultados Dork
            pdf.add_page()
            pdf.set_fill_color(*primary_color)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font(font_family, 'B', 16)
            pdf.cell(0, 15, 'Resultados de Búsquedas Dork',
                     new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.ln(5)

            pdf.set_font(font_family, '', 12)
            for dork, urls in self.results['dork_results'].items():
                pdf.set_text_color(*secondary_color)
                pdf.cell(0, 10, f'Búsqueda: {dork}',
                         new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(0, 0, 0)
                for url in urls:
                    pdf.cell(0, 10, f'  - {url}',
                             new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)

            # Guardar PDF
            output_file = os.path.join(
                self.hallazgos_dir, f"reconbot_{self.domain.replace('.', '_')}_report.pdf")
            pdf.output(output_file)
            print(f"\n[+] Informe PDF generado: {output_file}")

        except Exception as e:
            print(f"Error al generar el informe PDF: {str(e)}")

    def run_analysis(self) -> Dict[str, Any]:
        """Ejecuta el análisis completo."""
        print(f"\n[*] Iniciando análisis del dominio: {self.domain}")

        print("\n[+] Obteniendo registros DNS...")
        self.get_dns_records()

        print("\n[+] Obteniendo información WHOIS...")
        self.get_whois_info()

        print("\n[+] Realizando búsquedas Dork...")
        self.perform_dorking()

        print("\n[+] Analizando resultados con IA...")
        self.analyze_with_ai()

        print("\n[+] Generando resumen con OpenAI...")
        ai_summary = self.generate_ai_summary()

        print("\n[+] Generando informes...")
        self.generate_pdf_report(ai_summary)
        self.generate_html_report(ai_summary)

        return self.results


def main():
    parser = argparse.ArgumentParser(
        description="ReconBot - Herramienta de Reconocimiento Automatizado")
    parser.add_argument("domain", help="Dominio objetivo para el análisis")
    args = parser.parse_args()

    reconbot = ReconBot(args.domain)
    results = reconbot.run_analysis()

    # Guardar resultados en un archivo JSON
    output_file = os.path.join(
        "hallazgos", f"reconbot_{args.domain.replace('.', '_')}.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\n[+] Análisis completado. Resultados guardados en: {output_file}")


if __name__ == "__main__":
    main()
