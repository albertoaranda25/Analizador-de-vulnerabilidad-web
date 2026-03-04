import json
from datetime import datetime

class ReportGenerator:
    """Clase auxiliar para generar informes de las auditorías."""

    @staticmethod
    def export_to_json(networks: dict, filename: str = None):
        """
        Exporta el diccionario de redes descubiertas a un archivo JSON.
        Si no se da un nombre, genera uno automáticamente con la fecha y hora.
        """
        if not networks:
            print("\n[-] No se encontraron redes. No se generará informe.")
            return

        # Generamos un nombre de archivo único si no nos lo proporcionan
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"owisam_report_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # indent=4 lo formatea bonito para que sea legible por humanos
                json.dump(networks, f, indent=4, ensure_ascii=False)
            
            # Usamos colores estándar de terminal para el mensaje de éxito
            print(f"\n[\033[92m+\033[0m] Informe JSON generado con éxito: \033[1m{filename}\033[0m")
        except Exception as e:
            print(f"\n[\033[91m!\033[0m] Error al guardar el informe: {e}")