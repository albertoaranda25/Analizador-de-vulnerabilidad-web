# Analizador-de-vulnerabilidad-web
Analizador de vulnerabilidad. Utilizando Raw Sockets y análisis de tráfico 802.11 para detectar la ausencia del protocolo de protección 802.11w (MFP).

# 📡 OWISAM-DS: Simulador Pasivo de Ataques de Desautenticación (802.11)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

## 📖 Descripción del proyecto

Este proyecto es una herramienta de auditoría de seguridad Wi-Fi desarrollada **completamente desde cero** (sin el uso de suites de terceros como Aircrack-ng, Scapy, etc.). Su objetivo principal es cumplir con los requisitos de la metodología **OWISAM-DS (Pruebas de denegación de servicio)**.

A diferencia de las herramientas ofensivas tradicionales que interrumpen el servicio de forma activa, esta herramienta actúa como un **analizador de vulnerabilidad pasivo**. Utilizando **Raw Sockets** y análisis de tráfico 802.11 a nivel de bit, el software inspecciona las tramas de gestión (Beacon frames) de las redes cercanas para detectar la presencia o ausencia del protocolo de protección **802.11w (Management Frame Protection - MFP)**. 

El resultado es una **simulación matemática** que evalúa la resistencia de la red frente a ataques DoS y calcula el número de Puntos de Acceso (APs) y clientes que se verían afectados en un escenario real, todo ello sin generar ningún impacto en entornos de producción.

---

## ⚙️ Requerimientos

Para ejecutar esta herramienta, el sistema debe cumplir con los siguientes requisitos físicos y de software:

* **Sistema Operativo:** Distribución basada en GNU/Linux (Kali, Ubuntu, Debian, Parrot, etc.).
* **Hardware:** Tarjeta de red inalámbrica compatible con **Modo Monitor** (chipsets recomendados: Atheros, Ralink, Realtek).
* **Lenguaje:** Python 3.8 o superior (usando únicamente librerías estándar nativas: `socket`, `struct`, `os`).
* **Permisos:** Privilegios de superusuario (`root`) para la apertura de Raw Sockets y el cambio de estado de la interfaz de red.

---

## 🚀 Guía de instalación

Dado que el proyecto no posee dependencias externas ni librerías de terceros, la instalación consiste únicamente en clonar el repositorio y preparar la interfaz de red.

```zsh
# 1. Clonar el repositorio
git clone [https://github.com/tu-usuario/owisam-ds-simulator.git](https://github.com/tu-usuario/owisam-ds-simulator.git)

# 2. Acceder al directorio del proyecto
cd owisam-ds-simulator

# 3. Dar permisos de ejecución al script principal
chmod +x owisam_simulator.py
