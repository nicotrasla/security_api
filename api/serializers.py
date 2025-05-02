# api/serializers.py
from rest_framework import serializers
from core.domain.entities import GoogleDorkResult, DNSRecord, WhoisInfo, NmapScanResult

class GoogleDorkResultSerializer(serializers.Serializer):
    query = serializers.CharField()
    results = serializers.ListField()

class DNSRecordSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()

class WhoisInfoSerializer(serializers.Serializer):
    domain = serializers.CharField()
    registrar = serializers.CharField()
    creation_date = serializers.CharField()

class NmapPortSerializer(serializers.Serializer):
    port = serializers.IntegerField()
    state = serializers.CharField()
    service = serializers.CharField(required=False, allow_null=True)
    version = serializers.CharField(required=False, allow_null=True)

class NmapScanResultSerializer(serializers.Serializer):
    target = serializers.CharField()
    ports = NmapPortSerializer(many=True)
