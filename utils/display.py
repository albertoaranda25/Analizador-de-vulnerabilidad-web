class Display:
    """Clase para manejar los colores y el formato visual en la terminal."""
    
    # Códigos ANSI para colores
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def print_banner():
        """Imprime el logo de la herramienta al iniciar."""
        # Usamos r""" para que las barras invertidas se dibujen tal cual
        banner = r"""
  _______      __      ________ _____         __  __        _____   _____ 
 / __  \ \    /  \    / /_   _|/ ____|  /\   |  \/  |      |  __ \ / ____|
| |  | |\ \  / /\ \  / /  | | | (___   /  \  | \  / |______| |  | | (___  
| |  | | \ \/ /  \ \/ /   | |  \___ \ / /\ \ | |\/| |______| |  | |\___ \ 
| |__| |  \  /    \  /   _| |_ ____) / ____ \| |  | |      | |__| |____) |
 \____/    \/      \/   |_____|_____/_/    \_\_|  |_|      |_____/|_____/ 
        """
        print(f"{Display.CYAN}{Display.BOLD}{banner}{Display.RESET}")
        print(f"{Display.YELLOW}[*] Simulador OWISAM-DS - Detección de Deauth (802.11w){Display.RESET}\n")

    @staticmethod
    def print_table_header():
        """Imprime la cabecera de la tabla de resultados."""
        print(f"{Display.BOLD}{'BSSID':<19} | {'CH':<4} | {'SSID':<25} | {'ESTADO MFP / VULNERABILIDAD'}{Display.RESET}")
        print("-" * 87)

    @staticmethod
    def print_network_row(bssid: str, canal: str, ssid: str, status: str, is_vulnerable: bool):
        """Imprime una fila de la tabla con los colores adecuados."""
        # Convertimos el canal a string por si nos llega como un número entero
        ch_str = str(canal)
        
        # Recortamos el SSID si es muy largo para que no rompa la tabla (máximo 24 chars)
        ssid_display = ssid[:24] + (ssid[24:] and '…') 
        
        if is_vulnerable:
            vuln_text = f"{Display.RED}{Display.BOLD}[VULNERABLE] {status}{Display.RESET}"
        else:
            vuln_text = f"{Display.GREEN}{Display.BOLD}[SEGURO] {status}{Display.RESET}"
            
        # Añadimos la columna del canal (ch_str:<4) justo después del BSSID
        print(f"{bssid:<19} | {ch_str:<4} | {ssid_display:<25} | {vuln_text}")