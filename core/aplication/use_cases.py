from core.domain.services import GoogleDorkScanner, DnsScanner, WhoisScanner, NmapScanner
from core.domain.entities import GoogleDorkResult, DNSRecord, WhoisInfo, NmapScanResult
from typing import List

class GoogleDorkUseCase:
    def __init__(self, scanner: GoogleDorkScanner):
        self.scanner = scanner

    def execute(self, query: str) -> GoogleDorkResult:
        return self.scanner.scan(query)

class DnsScanUseCase:
    def __init__(self, scanner: DnsScanner):
        self.scanner = scanner

    def execute(self, domain: str, record_type: str) -> List[DNSRecord]:
        return self.scanner.scan(domain, record_type)

class WhoisScanUseCase:
    def __init__(self, scanner: WhoisScanner):
        self.scanner = scanner

    def execute(self, domain: str) -> WhoisInfo:
        return self.scanner.scan(domain)

class NmapScanUseCase:
    def __init__(self, scanner: NmapScanner):
        self.scanner = scanner

    def execute(self, target: str, ports: str = None) -> NmapScanResult:
        return self.scanner.scan(target, ports)
