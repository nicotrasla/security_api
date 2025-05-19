from django.urls import path
from .views import (
    GoogleDorkView,
    DnsScanView,
    WhoisScanView,
    NmapScanView,
    AIAnalysisView,
    home_page,
    custom_page_not_found,
    custom_server_error,
    trigger_error_500
)
from django.conf.urls import handler404, handler500
from django.views.generic import TemplateView

# Configuración de las rutas
urlpatterns = [
    # Página de inicio
    path('', home_page, name='home'),

    # Endpoint para probar error 500
    path('error-500/', trigger_error_500),

    # Rutas para las páginas informativas (GET)
    path('google-dork/info/', TemplateView.as_view(template_name="google_dork.html"),
         name='google-dork-info'),
    path('dns-scan/info/', TemplateView.as_view(template_name="dns_scan.html"),
         name='dns-scan-info'),
    path('whois-scan/info/', TemplateView.as_view(template_name="whois_scan.html"),
         name='whois-scan-info'),
    path('nmap-scan/info/', TemplateView.as_view(template_name="nmap_scan.html"),
         name='nmap-scan-info'),

    # Rutas para los endpoints funcionales (POST)
    path('api/google-dork/', GoogleDorkView.as_view(), name='google-dork'),
    path('api/dns-scan/', DnsScanView.as_view(), name='dns-scan'),
    path('api/whois-scan/', WhoisScanView.as_view(), name='whois-scan'),
    path('api/nmap-scan/', NmapScanView.as_view(), name='nmap-scan'),
    path('api/analyze/', AIAnalysisView.as_view(), name='ai-analyze'),
]

# Configuración de manejadores de errores
handler404 = custom_page_not_found
handler500 = custom_server_error
