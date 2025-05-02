from core.infrastructure.scanners.google_dorks import GoogleDorkScannerImpl
from core.infrastructure.scanners.dns_scan import DnsScannerImpl
from core.infrastructure.scanners.whois_scan import WhoisScannerImpl
from core.infrastructure.scanners.nmap_scan import NmapScannerImpl
from core.application.use_cases import GoogleDorkUseCase, DnsScanUseCase, WhoisScanUseCase, NmapScanUseCase

def create_google_dork_use_case() -> GoogleDorkUseCase:
    return GoogleDorkUseCase(GoogleDorkScannerImpl())

def create_dns_scan_use_case() -> DnsScanUseCase:
    return DnsScanUseCase(DnsScannerImpl())

def create_whois_scan_use_case() -> WhoisScanUseCase:
    return WhoisScanUseCase(WhoisScannerImpl())

def create_nmap_scan_use_case() -> NmapScanUseCase:
    return NmapScanUseCase(NmapScannerImpl())
