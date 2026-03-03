import struct

class RSNAnalyzer:
    """
    Analizador del Information Element (IE) Robust Security Network (RSN - Tag 48).
    Evalúa si la red soporta o requiere 802.11w (Management Frame Protection).
    """

    @staticmethod
    def analyze_mfp(tags_data: bytes) -> dict:
        pos = 0
        
        # Recorremos los tags igual que hicimos buscando el SSID
        while pos < len(tags_data) - 1:
            tag_num = tags_data[pos]
            tag_len = tags_data[pos + 1]
            tag_body = tags_data[pos + 2 : pos + 2 + tag_len]
            
            # Si encontramos el Tag 48 (RSN)
            if tag_num == 48:
                try:
                    # El campo RSN tiene longitud variable. Hay que calcular el desplazamiento (offset)
                    # Saltamos Version (2 bytes) y Group Cipher (4 bytes) -> Total 6 bytes
                    offset = 6
                    
                    # Leemos cuántos Pairwise Ciphers hay y los saltamos (4 bytes cada uno)
                    p_count = struct.unpack('<H', tag_body[offset:offset+2])[0]
                    offset += 2 + (4 * p_count)
                    
                    # Leemos cuántos AKM Suites hay y los saltamos (4 bytes cada uno)
                    a_count = struct.unpack('<H', tag_body[offset:offset+2])[0]
                    offset += 2 + (4 * a_count)
                    
                    # ¡Bingo! Hemos llegado a los 2 bytes de RSN Capabilities
                    rsn_cap = tag_body[offset:offset+2]
                    
                    if len(rsn_cap) >= 2:
                        cap_val = struct.unpack('<H', rsn_cap)[0]
                        
                        # Extraemos los bits 6 y 7 mediante operaciones bitwise
                        mfpr = (cap_val >> 6) & 1  # MFP Required (Requerido)
                        mfpc = (cap_val >> 7) & 1  # MFP Capable (Soportado)
                        
                        if mfpr == 1:
                            return {"status": "Seguro (MFP Requerido)", "vulnerable": False}
                        elif mfpc == 1:
                            return {"status": "Parcial (MFP Soportado pero no forzado)", "vulnerable": True}
                        else:
                            return {"status": "Vulnerable (MFP No Soportado)", "vulnerable": True}
                
                except Exception:
                    # Si la estructura RSN está malformada, asumimos vulnerabilidad por seguridad
                    pass 
            
            # Avanzamos al siguiente Tag
            pos += 2 + tag_len
            
        # Si termina el bucle y no hay Tag 48, es una red Abierta o WEP (Súper vulnerable)
        return {"status": "Vulnerable (Red Abierta o antigua)", "vulnerable": True}