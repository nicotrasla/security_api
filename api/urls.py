# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from api.serializers import GoogleDorkResultSerializer, DNSRecordSerializer, WhoisInfoSerializer, NmapScanResultSerializer
from core.infrastructure.adapters.scanner_adapter import (
    create_google_dork_use_case,
    create_dns_scan_use_case,
    create_whois_scan_use_case,
    create_nmap_scan_use_case,
)

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
        return Response(serializer.errors, status=status.HTTP_200_OK) # Corrected status code
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
    ports = serializers.CharField(required=False, allow_blank=True, default=None)

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
