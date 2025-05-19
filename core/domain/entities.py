from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GoogleDorkResult:
    query: str
    results: List[str]


@dataclass
class DNSRecord:
    type: str
    value: str


@dataclass
class WhoisInfo:
    registrar: str
    creation_date: str
    expiration_date: str
    name_servers: List[str]
    status: List[str]


@dataclass
class NmapScanResult:
    target: str
    ports: List[str]
    services: List[str]


@dataclass
class AIAnalysisResult:
    classification: str
    confidence: float
    details: Dict[str, Any]
