import socket
import struct

class RawSocketManager:
    def __init__(self, interface: str):
        self.interface = interface
        self.sock = None

    def open_socket(self):
        """Abre un raw socket vinculado a la interfaz en modo monitor."""
        try:
            # AF_PACKET: Bajo nivel (capa de enlace)
            # SOCK_RAW: Paquetes sin procesar por el kernel
            # 0x0003: Protocolo ETH_P_ALL (captura todo)
            self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            self.sock.bind((self.interface, 0))
            print(f"[+] Socket abierto exitosamente en {self.interface}")
        except PermissionError:
            print("[!] Error: Se requieren privilegios de ROOT (sudo).")
            raise
        except Exception as e:
            print(f"[!] Error al abrir el socket: {e}")
            raise

    def receive_packet(self):
        """Recibe un paquete individual de la interfaz."""
        if not self.sock:
            return None
        
        # Recibimos el paquete (el buffer de 2048 es suficiente para 802.11)
        packet, addr = self.sock.recvfrom(2048)
        return packet