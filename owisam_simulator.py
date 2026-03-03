import argparse
import sys

# Importamos nuestros módulos personalizados
from core.raw_sockets import RawSocketManager
from parsers.dot11_parser import Dot11Parser

def test_parser():
    """Función de laboratorio para probar el parser sin tarjeta de red."""
    print("[*] Ejecutando test de laboratorio (Sin antena)...")
    
    # Esto es una trama Beacon real convertida a bytes.
    # Contiene la cabecera Radiotap, un BSSID y un SSID llamado "Mi_Wifi_Test"
    mock_packet = bytes.fromhex(
        "000012002e48000000028509a000c0000000" # Radiotap (18 bytes)
        "80000000"                             # Frame Control y Duración
        "ffffffffffff"                         # Destino (Broadcast)
        "112233445566"                         # Origen (Router MAC)
        "112233445566"                         # BSSID (Router MAC)
        "0000"                                 # Seq Control
        "000000000000000000000000"             # Parámetros fijos (12 bytes)
        "000c4d695f576966695f54657374"         # Tag 0 (SSID: "Mi_Wifi_Test", longitud 12)
    )
    
    resultado = Dot11Parser.parse_beacon(mock_packet)
    
    if resultado:
        print(f"[+] ¡Éxito! Trama parseada correctamente.")
        print(f"    - BSSID Encontrado: {resultado['bssid']}")
        print(f"    - SSID Encontrado:  {resultado['ssid']}")
    else:
        print("[-] Fallo al parsear la trama.")


def main():
    # 1. Configurar los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(
        description="OWISAM-DS: Simulador de Denegación de Servicio Wi-Fi (802.11w)"
    )
    
    # Argumento para la interfaz de red (ahora es opcional para permitir el --test)
    parser.add_argument(
        "-i", "--interface", 
        help="Interfaz de red en modo monitor (ej. wlan0mon)"
    )
    
    # Argumento para el tiempo de escaneo
    parser.add_argument(
        "-t", "--time", 
        type=int, 
        default=60, 
        help="Tiempo de escaneo en segundos (por defecto: 60)"
    )
    
    # Argumento especial para ejecutar el test sin hardware
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Ejecuta una prueba de laboratorio sin necesidad de tarjeta Wi-Fi"
    )

    args = parser.parse_args()

    # 2. Lógica de ejecución
    if args.test:
        test_parser()
        sys.exit(0) # Salimos limpiamente después del test

    if not args.interface:
        print("[!] Error: Debes especificar una interfaz con -i o usar --test para probar.")
        parser.print_help()
        sys.exit(1)

    # 3. Si hay interfaz, iniciamos el socket real
    print(f"[*] Iniciando auditoría OWISAM-DS en {args.interface}...")
    
    try:
        connection = RawSocketManager(args.interface)
        connection.open_socket()
        
        # Aquí irá el bucle de captura en el futuro
        print(f"[+] Escaneando durante {args.time} segundos. Presiona Ctrl+C para detener.")
        
    except Exception as e:
        print(f"\n[!] Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()