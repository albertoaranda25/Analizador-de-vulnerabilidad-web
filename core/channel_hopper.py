import time
import threading
import subprocess

class ChannelHopper:
    """
    Clase encargada de cambiar el canal de la interfaz Wi-Fi en segundo plano
    para poder descubrir Redes/APs en todo el espectro.
    """
    def __init__(self, interface: str, channels: list = None):
        self.interface = interface
        # Si no le pasamos canales, usa los 13 canales estándar de 2.4 GHz en Europa
        self.channels = channels if channels else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.is_hopping = False
        self.hop_thread = None

    def start(self):
        """Inicia el hilo en segundo plano para saltar de canal."""
        self.is_hopping = True
        # daemon=True hace que el hilo se cierre automáticamente si el programa principal termina
        self.hop_thread = threading.Thread(target=self._hop, daemon=True)
        self.hop_thread.start()
        print(f"[*] Iniciando barrido de canales (Channel Hopping) en {self.interface}...")

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
                    # Tiempo de espera en cada canal (0.5 segundos es un buen equilibrio)
                    time.sleep(0.5)
                except Exception:
                    # Si falla (ej. la tarjeta se desconectó), ignoramos y seguimos intentando
                    pass