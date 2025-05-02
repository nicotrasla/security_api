from core.domain.services import WhoisScanner
from core.domain.entities import WhoisInfo
import whois

class WhoisScannerImpl(WhoisScanner):
    def scan(self, domain: str) -> WhoisInfo:
        try:
            whois_info = whois.whois(domain)
            return WhoisInfo(
                domain=whois_info.domain[0] if isinstance(whois_info.domain, list) and whois_info.domain else whois_info.domain,
                registrar=whois_info.registrar[0] if isinstance(whois_info.registrar, list) and whois_info.registrar else whois_info.registrar,
                creation_date=str(whois_info.creation_date[0] if isinstance(whois_info.creation_date, list) and whois_info.creation_date else whois_info.creation_date),
            )
        except whois.DomainInvalid:
            return WhoisInfo(domain=domain, registrar="N/A", creation_date="N/A")
        except Exception as e:
            return WhoisInfo(domain=domain, registrar="Error", creation_date=str(e))
