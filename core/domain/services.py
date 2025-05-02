from typing import Protocol,List
from .entities import GoogleDorkResult, DNSRecord, WhoisInfo, NmapScanResult

class GoogleDorkScanner(Protocol):
    def scan(self, query: str) -> GoogleDorkResult:
        ...

class DnsScanner(Protocol):
    def scan(self, domain: str, record_type: str) -> List[DNSRecord]:
        ...

class WhoisScanner(Protocol):
    def scan(self, domain: str) -> WhoisInfo:
        ...

class NmapScanner(Protocol):
    def scan(self, target: str, ports: str = None) -> NmapScanResult:
        ...
