# api/serializers.py
from rest_framework import serializers
from core.domain.entities import GoogleDorkResult, DNSRecord, WhoisInfo, NmapScanResult


class GoogleDorkResultSerializer(serializers.Serializer):
    query = serializers.CharField()
    results = serializers.ListField(child=serializers.CharField())


class DNSRecordSerializer(serializers.Serializer):
    type = serializers.CharField()
    value = serializers.CharField()


class WhoisInfoSerializer(serializers.Serializer):
    registrar = serializers.CharField()
    creation_date = serializers.CharField()
    expiration_date = serializers.CharField()
    name_servers = serializers.ListField(child=serializers.CharField())
    status = serializers.ListField(child=serializers.CharField())


class NmapPortSerializer(serializers.Serializer):
    port = serializers.IntegerField()
    state = serializers.CharField()
    service = serializers.CharField(required=False, allow_null=True)
    version = serializers.CharField(required=False, allow_null=True)


class NmapScanResultSerializer(serializers.Serializer):
    target = serializers.CharField()
    ports = serializers.ListField(child=serializers.CharField())
    services = serializers.ListField(child=serializers.CharField())


class AIAnalysisRequestSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)


class AIAnalysisResponseSerializer(serializers.Serializer):
    classification = serializers.CharField()
    confidence = serializers.FloatField()
    details = serializers.DictField()
