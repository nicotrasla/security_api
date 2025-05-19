# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from api.serializers import (
    GoogleDorkResultSerializer,
    DNSRecordSerializer,
    WhoisInfoSerializer,
    NmapScanResultSerializer,
    AIAnalysisRequestSerializer,
    AIAnalysisResponseSerializer
)
from core.infrastructure.adapters.scanner_adapter import (
    create_google_dork_use_case,
    create_dns_scan_use_case,
    create_whois_scan_use_case,
    create_nmap_scan_use_case,
)
from django.shortcuts import render
from django.http import HttpResponseServerError
import json
import re


def trigger_error_500(request):
    # Genera un error 500 intencionalmente
    raise Exception("Error 500 generado intencionalmente para pruebas.")


def home_page(request):
    return render(request, 'home.html')


def custom_page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def custom_server_error(request):
    return render(request, '500.html', status=500)


class GoogleDorkRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)


class GoogleDorkView(APIView):
    def post(self, request):
        serializer = GoogleDorkRequestSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            use_case = create_google_dork_use_case()
            result = use_case.execute(query)
            result_serializer = GoogleDorkResultSerializer(result)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DnsScanRequestSerializer(serializers.Serializer):
    domain = serializers.CharField(required=True)
    type = serializers.CharField(default='A')


class DnsScanView(APIView):
    def post(self, request):
        serializer = DnsScanRequestSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data['domain']
            record_type = serializer.validated_data['type']
            use_case = create_dns_scan_use_case()
            results = use_case.execute(domain, record_type)
            result_serializer = DNSRecordSerializer(results, many=True)
            return Response(result_serializer.data)
        # Corrected status code
        return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WhoisScanRequestSerializer(serializers.Serializer):
    domain = serializers.CharField(required=True)


class WhoisScanView(APIView):
    def post(self, request):
        serializer = WhoisScanRequestSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data['domain']
            use_case = create_whois_scan_use_case()
            result = use_case.execute(domain)
            result_serializer = WhoisInfoSerializer(result)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NmapScanRequestSerializer(serializers.Serializer):
    target = serializers.CharField(required=True)
    ports = serializers.CharField(
        required=False, allow_blank=True, default=None)


class NmapScanView(APIView):
    def post(self, request):
        serializer = NmapScanRequestSerializer(data=request.data)
        if serializer.is_valid():
            target = serializer.validated_data['target']
            ports = serializer.validated_data['ports']
            use_case = create_nmap_scan_use_case()
            result = use_case.execute(target, ports)
            result_serializer = NmapScanResultSerializer(result)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIAnalysisView(APIView):
    def post(self, request):
        serializer = AIAnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']

            # Análisis básico de seguridad
            sensitive_patterns = {
                'config_files': r'\.(env|xml|conf|config|ini|yaml|yml)$',
                'backup_files': r'\.(bak|backup|old|tmp|temp)$',
                'admin_pages': r'(admin|login|dashboard|control|manage)',
                'sensitive_dirs': r'(backup|db|database|sql|logs|log)',
                'api_endpoints': r'(api|rest|graphql|soap)',
            }

            results = json.loads(text)
            analysis = {
                'classification': 'neutral',
                'confidence': 0.0,
                'details': {
                    'sensitive_files': [],
                    'potential_vulnerabilities': [],
                    'recommendations': []
                }
            }

            for dork, urls in results.items():
                for url in urls:
                    # Analizar cada URL
                    for pattern_name, pattern in sensitive_patterns.items():
                        if re.search(pattern, url, re.IGNORECASE):
                            if pattern_name in ['config_files', 'backup_files']:
                                analysis['details']['sensitive_files'].append(
                                    url)
                                analysis['classification'] = 'potentially_sensitive'
                                analysis['confidence'] = max(
                                    analysis['confidence'], 0.7)
                            elif pattern_name in ['admin_pages', 'sensitive_dirs']:
                                analysis['details']['potential_vulnerabilities'].append(
                                    url)
                                analysis['classification'] = 'potentially_sensitive'
                                analysis['confidence'] = max(
                                    analysis['confidence'], 0.8)
                            elif pattern_name == 'api_endpoints':
                                analysis['details']['potential_vulnerabilities'].append(
                                    url)
                                analysis['classification'] = 'potentially_sensitive'
                                analysis['confidence'] = max(
                                    analysis['confidence'], 0.6)

            # Generar recomendaciones basadas en los hallazgos
            if analysis['details']['sensitive_files']:
                analysis['details']['recommendations'].append(
                    "Se encontraron archivos de configuración o respaldo expuestos. "
                    "Considere restringir el acceso a estos archivos."
                )
            if analysis['details']['potential_vulnerabilities']:
                analysis['details']['recommendations'].append(
                    "Se detectaron páginas administrativas o directorios sensibles. "
                    "Verifique que estos recursos estén adecuadamente protegidos."
                )

            result_serializer = AIAnalysisResponseSerializer(analysis)
            return Response(result_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
