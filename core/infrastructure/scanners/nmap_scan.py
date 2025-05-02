# core/infrastructure/scanners/nmap_scan.py
from core.domain.services import NmapScanner
from core.domain.entities import NmapScanResult
import nmap

class NmapScannerImpl(NmapScanner):
    def scan(self, target: str, ports: str = None) -> NmapScanResult:
        nm = nmap.PortScanner()
        try:
            scan_results = nm.scan(hosts=target, ports=ports, arguments='-sS -sV')  # SYN scan y detección de versión
            ports_data = []
            if target in scan_results['scan']:
                for port, port_info in scan_results['scan'][target]['tcp'].items():
                    ports_data.append({"port": port, "state": port_info['state'], "service": port_info['name'], "version": port_info['product'] + " " + port_info['version']})
            return NmapScanResult(target=target, ports=ports_data)
        except Exception as e:
            return NmapScanResult(target=target, ports=[{"error": str(e)}])

# Asegúrate de tener nmap instalado en tu sistema y la librería python-nmap:
# pip install python-nmap
