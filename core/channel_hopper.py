import time
import threading
import subprocess

class ChannelHopper:
    """
    Clase encargada de cambiar el canal de la interfaz Wi-Fi en segundo plano
    para poder descubrir Redes/APs en todo el espectro (2.4 GHz y 5 GHz).
    """
    def __init__(self, interface: str, channels: list = None):
        self.interface = interface
        # Añadimos los canales de 5 GHz más comunes al espectro de 2.4 GHz
        self.channels = channels if channels else [
            # Banda 2.4 GHz (Canales europeos)
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            # Banda 5 GHz (U-NII-1, U-NII-2A, U-NII-2C, U-NII-3)
            36, 40, 44, 48, 52, 56, 60, 64, 
            100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140,
            149, 153, 157, 161, 165
        ]
        self.is_hopping = False
        self.hop_thread = None

    def start(self):
        """Inicia el hilo en segundo plano para saltar de canal."""
        self.is_hopping = True
        # daemon=True hace que el hilo se cierre automáticamente si el programa principal termina
        self.hop_thread = threading.Thread(target=self._hop, daemon=True)
        self.hop_thread.start()
        print(f"[*] Iniciando barrido Multi-Banda (2.4GHz + 5GHz) en {self.interface}...")

    def stop(self):
        """Detiene el salto de canales de forma segura."""
        self.is_hopping = False
        if self.hop_thread:
            self.hop_thread.join() # Espera a que el hilo termine limpiamente
        print("\n[*] Barrido de canales detenido.")

    def _hop(self):
        """Método interno que ejecuta el bucle infinito de saltos."""
        while self.is_hopping:
            for channel in self.channels:
                if not self.is_hopping:
                    break
                
                try:
                    # Ejecuta el comando de Linux: iw dev wlan0mon set channel X
                    subprocess.run(
                        ['iw', 'dev', self.interface, 'set', 'channel', str(channel)],
                        stdout=subprocess.DEVNULL, # Oculta la salida estándar
                        stderr=subprocess.DEVNULL  # Oculta los errores
                    )
                    # Tiempo de espera en cada canal. 
                    # 0.3s * 35 canales = ~10 segundos en dar una vuelta completa al espectro.
                    time.sleep(0.3)
                except Exception:
                    # Si falla (ej. la tarjeta no soporta un canal concreto), ignoramos y seguimos
                    pass