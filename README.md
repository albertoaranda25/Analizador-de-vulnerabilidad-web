# 📡 OWISAM: Analizador de vulnerabilidad web (802.11)

![License](https://img.shields.io/badge/license-EUSA-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

## 📖 Descripción del proyecto

Este proyecto es una herramienta de auditoría de seguridad Wi-Fi desarrollada sin el uso de suites de terceros como Aircrack-ng, Scapy, etc. Su objetivo principal es cumplir con los requisitos de la metodología **OWISAM-DS (Pruebas de denegación de servicio)**.

La herramienta opera en dos fases diferenciadas:

1. **Análisis Pasivo:** Utilizando Raw Sockets y análisis de tráfico 802.11 a nivel de bit, inspecciona las tramas de gestión (Beacon frames) para extraer el BSSID, SSID, el Canal de operación y detectar la presencia o ausencia del protocolo de protección **802.11w (Management Frame Protection - MFP)**.
2. **Explotación Activa (Simulación DoS):** Permite aislar el canal específico de un objetivo vulnerable y lanzar ráfagas de desautenticación (Deauth) dirigidas para evaluar la resistencia real de la red frente a interrupciones de servicio.

Todo ello se consolida en reportes estructurados (JSON), proporcionando una visión clara del impacto en un entorno real.

---

## ⚙️ Requerimientos

Para ejecutar esta herramienta, el sistema debe cumplir con los siguientes requisitos físicos y de software:

* **Sistema Operativo:** Distribución basada en GNU/Linux (Kali, Ubuntu, Debian, Parrot, etc.).
* **Hardware:** Tarjeta de red inalámbrica compatible con **Modo Monitor** e inyección de paquetes (chipsets recomendados: Atheros, Ralink, Realtek).
* **Lenguaje:** Python 3.8 o superior.
* **Permisos:** Privilegios de superusuario (`root`) para la apertura de Raw Sockets, inyección de paquetes y el cambio de estado de la interfaz de red.

---

## 🚀 Guía de instalación y uso

Dado que el proyecto está diseñado para ser autónomo, la instalación consiste únicamente en clonar el repositorio y preparar la interfaz de red.

```zsh
# 1. Clonar el repositorio
git clone [https://github.com/albertoaranda25/Analizador-de-vulnerabilidad-web.git](https://github.com/albertoaranda25/Analizador-de-vulnerabilidad-web.git)

# 2. Acceder al directorio del proyecto
cd Analizador-de-vulnerabilidad-web

# 3. Dar permisos de ejecución al script principal
chmod +x owisam_simulator.py

# 4. Poner tu tarjeta de red en Modo Monitor (Sustituye 'wlan0' por tu interfaz)

# 4.1. Matamos los procesos que molestan ANTES de hacer nada
sudo airmon-ng check kill

# 4.2. Apagamos el ahorro de energía en la interfaz original
sudo iw dev wlan0 set power_save off

# 4.3. Tiramos la interfaz abajo
sudo ip link set wlan0 down

# 4.4. Cambiamos su modo a monitor (¡sin cambiarle el nombre!)
sudo iw dev wlan0 set type monitor

# 4.5. La volvemos a levantar
sudo ip link set wlan0 up

# 5. Ejecutar la herramienta (requiere permisos de root)
sudo python3 owisam_simulator.py
