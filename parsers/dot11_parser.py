import struct

class Dot11Parser:
    """
    Clase encargada de desempaquetar y traducir tramas 802.11 a nivel de bytes
    sin utilizar dependencias externas.
    """

    @staticmethod
    def parse_beacon(packet: bytes):
        # 1. SALTAR LA CABECERA RADIOTAP
        # Cuando capturamos en modo monitor, el sistema operativo añade una cabecera
        # llamada "Radiotap" al principio. Su longitud es variable.
        # Los bytes 2 y 3 (índices 2:4) indican su tamaño exacto en formato Little-Endian.
        if len(packet) < 4:
            return None
            
        radiotap_len = struct.unpack('<H', packet[2:4])[0]
        
        # Recortamos el paquete para quedarnos solo con la trama 802.11 real
        dot11_frame = packet[radiotap_len:]
        
        # Una cabecera 802.11 mínima tiene 24 bytes. Si es menor, está corrupta.
        if len(dot11_frame) < 24:
            return None

        # 2. LEER EL FRAME CONTROL (Byte 0)
        # Aquí sabemos si es una trama de gestión, de datos, etc.
        frame_control = dot11_frame[0]
        
        # Operaciones a nivel de bit (Bitwise) para extraer Tipo y Subtipo
        f_type = (frame_control >> 2) & 3      # Tipo: 0 = Gestión (Management)
        f_subtype = (frame_control >> 4) & 15  # Subtipo: 8 = Beacon
        
        # Si no es un Beacon Frame de gestión, lo ignoramos y devolvemos None
        if f_type != 0 or f_subtype != 8:
            return None

        # 3. EXTRAER DIRECCIÓN MAC (BSSID)
        # En las tramas de gestión, la Dirección 3 (bytes 16 al 21) es el BSSID
        bssid_bytes = dot11_frame[16:22]
        # Formateamos los bytes a texto: "AA:BB:CC:DD:EE:FF"
        bssid = ':'.join(f'{b:02x}' for b in bssid_bytes).upper()

        # 4. EXTRAER EL NOMBRE DE LA RED (SSID)
        # En un Beacon, después de la cabecera (24 bytes) hay 12 bytes fijos 
        # (Timestamp, Intervalo, Capacidades). Los "Tags" empiezan en el byte 36.
        tags_data = dot11_frame[36:]
        
        ssid = "<Oculto>"
        pos = 0
        
        # Bucle para leer los Tags (Etiquetas)
        while pos < len(tags_data) - 1:
            tag_num = tags_data[pos]       # Qué información es (0 = SSID, 48 = RSN)
            tag_len = tags_data[pos + 1]   # Cuánto ocupa esa información
            pos += 2                       # Avanzamos a los datos reales
            
            # Si el Tag es el 0, hemos encontrado el SSID
            if tag_num == 0:
                try:
                    ssid = tags_data[pos : pos + tag_len].decode('utf-8', errors='ignore')
                except:
                    pass
                break # Ya tenemos el nombre, salimos del bucle
                
            pos += tag_len # Saltamos al siguiente Tag

        return {
            "bssid": bssid,
            "ssid": ssid,
            "raw_tags": tags_data # Guardamos el resto de tags para analizarlos luego (802.11w)
        }