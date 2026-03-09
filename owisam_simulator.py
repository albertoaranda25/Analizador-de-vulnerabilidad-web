import argparse
import sys
import time
from utils.display import Display
from utils.helpers import ReportGenerator

# Importamos nuestros módulos personalizados
from core.raw_sockets import RawSocketManager
from core.channel_hopper import ChannelHopper
from parsers.dot11_parser import Dot11Parser
from parsers.rsn_analyzer import RSNAnalyzer

def test_parser():
    """Función de laboratorio para probar el parser y el análisis RSN sin antena."""
    print("[*] Ejecutando test de laboratorio (Sin antena)...")
    
    mock_packet = bytes.fromhex(
        "000012002e48000000028509a000c000000080000000ffffffffffff"
        "1122334455661122334455660000000000000000000000000000"
        "000c4d695f576966695f54657374"
        "30140100000fac040100000fac040100000fac020000" 
    )
    
    resultado = Dot11Parser.parse_beacon(mock_packet)
    if resultado:
        print(f"[+] ¡Éxito! BSSID: {resultado['bssid']} | SSID: {resultado['ssid']}")
        
        # 1. PRIMERO calculamos el análisis
        analisis = RSNAnalyzer.analyze_mfp(resultado['raw_tags'])
        print(f"[*] Resultado OWISAM: {analisis['status']} -> Vulnerable: {analisis['vulnerable']}")
        
        # 2. DESPUÉS empaquetamos los datos y generamos el informe
        redes_simuladas = {
            resultado['bssid']: {
                'ssid': resultado['ssid'], 
                'vulnerable': analisis['vulnerable'], 
                'status': analisis['status']
            }
        }
        ReportGenerator.export_to_json(redes_simuladas, "test_report.json")
    else:
        print("[-] Fallo al parsear la trama.")

def main():

    Display.print_banner()

    parser = argparse.ArgumentParser(description="OWISAM-DS: Simulador de Denegación de Servicio Wi-Fi (802.11w)")
    parser.add_argument("-i", "--interface", help="Interfaz de red en modo monitor (ej. wlan0mon)")
    parser.add_argument("-t", "--time", type=int, default=60, help="Tiempo de escaneo en segundos (por defecto: 60)")
    parser.add_argument("--test", action="store_true", help="Ejecuta una prueba de laboratorio")

    args = parser.parse_args()

    if args.test:
        test_parser()
        sys.exit(0)

    if not args.interface:
        print("[!] Error: Debes especificar una interfaz con -i o usar --test para probar.")
        parser.print_help()
        sys.exit(1)

    print(f"[*] Iniciando auditoría OWISAM-DS en {args.interface}...")
    
    # Estructura para guardar las redes encontradas y no repetirlas
    redes_descubiertas = {}
    hopper = None

    try:
        # 1. Iniciamos el Socket
        conexion = RawSocketManager(args.interface)
        conexion.open_socket()
        
        # 2. Iniciamos el salto de canales en segundo plano
        hopper = ChannelHopper(args.interface)
        hopper.start()
        
        # 3. Bucle principal de captura
        print(f"[+] Escaneando durante {args.time} segundos. Presiona Ctrl+C para detener prematuramente.\n")
        
        # --- USAMOS LA NUEVA CABECERA ---
        Display.print_table_header()
        
        tiempo_fin = time.time() + args.time
        
        while time.time() < tiempo_fin:
            paquete = conexion.receive_packet()
            if not paquete:
                continue
                
            datos_beacon = Dot11Parser.parse_beacon(paquete)
            
            if datos_beacon and datos_beacon['bssid'] not in redes_descubiertas:
                bssid = datos_beacon['bssid']
                ssid = datos_beacon['ssid']
                tags = datos_beacon['raw_tags']
                
                analisis = RSNAnalyzer.analyze_mfp(tags)
                
                redes_descubiertas[bssid] = {
                    'ssid': ssid,
                    'vulnerable': analisis['vulnerable'],
                    'status': analisis['status']
                }
                
                # --- USAMOS LA NUEVA FILA A COLOR ---
                Display.print_network_row(bssid, ssid, analisis['status'], analisis['vulnerable'])

    except KeyboardInterrupt:
        print("\n[!] Escaneo interrumpido por el usuario (Ctrl+C).")
    except Exception as e:
        print(f"\n[!] Error crítico: {e}")
    finally:
        # 4. Limpieza al terminar
        if hopper:
            hopper.stop()
        
        print("\n[*] Auditoría finalizada.")
        print(f"[*] Total de redes únicas descubiertas: {len(redes_descubiertas)}")
        
        # 5. Guardar informe automáticamente
        if not args.test:  # Evitamos crear archivos basura cuando solo hacemos el --test rápido
            ReportGenerator.export_to_json(redes_descubiertas)

if __name__ == "__main__":
    main()