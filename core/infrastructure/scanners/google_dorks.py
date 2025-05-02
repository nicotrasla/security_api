# core/infrastructure/scanners/google_dorks.py
from core.domain.services import GoogleDorkScanner
from core.domain.entities import GoogleDorkResult
# Importa las librerías necesarias para tu script de Google Dorks (ej. googlesearch-python)
# pip install googlesearch-python

class GoogleDorkScannerImpl(GoogleDorkScanner):
    def scan(self, query: str) -> GoogleDorkResult:
        try:
            from googlesearch import search
            results_data = [{"title": result, "url": result} for result in search(query, num_results=10)]
            return GoogleDorkResult(query=query, results=results_data)
        except ImportError:
            return GoogleDorkResult(query=query, results=[{"error": "googlesearch-python no está instalado"}])
        except Exception as e:
            return GoogleDorkResult(query=query, results=[{"error": str(e)}])
