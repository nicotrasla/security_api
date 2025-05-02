# core/infrastructure/scanners/dns_scan.py
from core.domain.services import DnsScanner
from core.domain.entities import DNSRecord
import dns.resolver

class DnsScannerImpl(DnsScanner):
    def scan(self, domain: str, record_type: str) -> list[DNSRecord]:
        records = []
        try:
            for rdata in dns.resolver.resolve(domain, record_type):
                records.append(DNSRecord(type=record_type, value=str(rdata)))
        except dns.resolver.NXDOMAIN:
            records.append(DNSRecord(type=record_type, value=f"Dominio no encontrado: {domain}"))
        except dns.resolver.NoAnswer:
            records.append(DNSRecord(type=record_type, value=f"No se encontraron registros {record_type} para {domain}"))
        except Exception as e:
            records.append(DNSRecord(type=record_type, value=f"Error al realizar la consulta DNS: {e}"))
        return records
