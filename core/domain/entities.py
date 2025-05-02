from dataclasses import dataclass
from typing import List, Dict

@dataclass
class GoogleDorkResult:
    query: str
    results: List[Dict]

@dataclass
class DNSRecord:
    type: str
    value: str

@dataclass
class WhoisInfo:
    domain: str
    registrar: str
    creation_date: str

@dataclass
class NmapScanResult:
    target: str
    ports: List[Dict]
