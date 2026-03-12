import argparse
import sys
import time
from utils.display import Display
from utils.helpers import ReportGenerator
import subprocess
from core.deauth_attacker import DeauthAttacker

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
        
def main():
    while True:
        Display.print_banner()
        print("\n" + "="*50)
        print(" MENÚ PRINCIPAL - SIMULADOR OWISAM-DS v2.0")
        print("="*50)
        print(" [\033[92m1\033[0m] Modo Escáner (Auditoría pasiva de redes)")
        print(" [\033[94m2\033[0m] Modo Test (Laboratorio sin antena)")
        print(" [\033[91m3\033[0m] Modo Ataque (Denegación de Servicio - DoS)")
        print(" [\033[93m4\033[0m] Salir")
        print("="*50)
        
        opcion = input("\n[?] Selecciona una opción (1-4): ")

        if opcion == '1':
            print("\n[*] MODO ESCÁNER SELECCIONADO")
            interfaz = input("[>] Introduce tu interfaz en modo monitor (ej. wlan0mon): ")
            tiempo = input("[>] Introduce el tiempo de escaneo en segundos [Pulsar Enter para 60s]: ")
            tiempo = int(tiempo) if tiempo.isdigit() else 60
            
            print(f"\n[*] Iniciando auditoría en {interfaz} durante {tiempo} segundos...")
            
            # Inicializamos variables críticas antes del Try
            redes_descubiertas = {}
            hopper = None
            
            try:
                # 1. Iniciamos el Socket (CORREGIDO: usamos 'interfaz' en vez de 'args.interface')
                conexion = RawSocketManager(interfaz)
                conexion.open_socket()
        
                # 2. Iniciamos el salto de canales en segundo plano
                hopper = ChannelHopper(interfaz)
                hopper.start()
        
                # 3. Bucle principal de captura (CORREGIDO: usamos 'tiempo')
                print(f"[+] Escaneando durante {tiempo} segundos. Presiona Ctrl+C para detener prematuramente.\n")
        
                Display.print_table_header()
        
                tiempo_fin = time.time() + tiempo
        
                while time.time() < tiempo_fin:
                    paquete = conexion.receive_packet()
                    if not paquete:
                        continue
        
                    datos_beacon = Dot11Parser.parse_beacon(paquete)
            
                    if datos_beacon and datos_beacon['bssid'] not in redes_descubiertas:
                        bssid = datos_beacon['bssid']
                        ssid = datos_beacon['ssid']
                        tags = datos_beacon['raw_tags']

                        # Recogemos el canal del parser (si no lo encuentra, ponemos '?')
                        canal = datos_beacon.get('channel', '?')
                
                        analisis = RSNAnalyzer.analyze_mfp(tags)
                
                        redes_descubiertas[bssid] = {
                            'ssid': ssid,
                            'channel': canal,
                            'vulnerable': analisis['vulnerable'],
                            'status': analisis['status']
                        }
                
                        Display.print_network_row(bssid, canal, ssid, analisis['status'], analisis['vulnerable'])

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
            
            # 5. Guardar informe automáticamente (CORREGIDO: quitado el args.test)
            ReportGenerator.export_to_json(redes_descubiertas)
            input("\n[Pausa] Pulsa Enter para volver al menú principal...")

        # CORREGIDO: Los elif ahora están alineados correctamente con el primer if
        elif opcion == '2':
            print("\n[*] MODO TEST SELECCIONADO")
            test_parser()
            input("\n[Pausa] Pulsa Enter para volver al menú principal...")

        elif opcion == '3':
            print("\n[*] MODO OFENSIVO (DoS) SELECCIONADO")
            interfaz = input("[>] Introduce tu interfaz en modo monitor (ej. wlan0mon): ")
            bssid = input("[>] Introduce el BSSID (MAC) del objetivo (ej. AA:BB:CC:DD:EE:FF): ")
            canal = input("[>] Introduce el canal del objetivo (1-13): ")
            
            if canal.isdigit():
                print(f"[*] Fijando la interfaz {interfaz} en el canal {canal}...")
                subprocess.run(['iw', 'dev', interfaz, 'set', 'channel', canal], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print("[\033[93m!\033[0m] Advertencia: Canal no válido. El ataque fallará si no estás en el canal correcto.")
            
            # Lanzamos el ataque
            DeauthAttacker.start_attack(interface=interfaz, bssid=bssid, count=50)
            input("\n[Pausa] Pulsa Enter para volver al menú principal...")

        elif opcion == '4':
            print("\n[*] Saliendo del simulador OWISAM-DS. ¡Buena caza!\n")
            sys.exit(0)

        else:
            print("\n[-] Opción no válida. Por favor, elige un número del 1 al 4.")
            input("\nPulsa Enter para continuar...")   

if __name__ == "__main__":
    main()