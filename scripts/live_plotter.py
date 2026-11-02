"""
live_plotter.py
Adquisición y visualización gráfica en tiempo real de telemetría serial.
Proyecto: Sistema Híbrido de Sensado Electromagnético (INCIETEC 2026-2)
Autor: Gabriel Jaime Gómez Restrepo
"""

import sys
import os
import csv
import time
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Configuración de puerto y comunicación
BAUD_RATE = 115200
VENTANA_MUESTRAS = 60  # Muestra los últimos 60 puntos en pantalla

# Colas circulares para la visualización fluida
tiempos_s = deque(maxlen=VENTANA_MUESTRAS)
frecuencias_hz = deque(maxlen=VENTANA_MUESTRAS)
rpms = deque(maxlen=VENTANA_MUESTRAS)


def auto_detectar_puerto():
    """Detecta automáticamente el puerto COM/ttyUSB donde está el Arduino."""
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        desc = p.description.lower()
        if "ch340" in desc or "arduino" in desc or "usb-serial" in desc or "usb serial" in desc:
            return p.device
    if puertos:
        return puertos[0].device
    return None


puerto_serial = auto_detectar_puerto()
if not puerto_serial:
    print("[ERROR] No se detectó ninguna placa conectada por USB.")
    print("Conecta el Arduino Nano y vuelve a ejecutar el script.")
    sys.exit(1)

print(f"[CONECTADO] Abriendo puerto serial: {puerto_serial} a {BAUD_RATE} baudios...")
try:
    ser = serial.Serial(puerto_serial, BAUD_RATE, timeout=0.1)
    time.sleep(2.0)  # Tiempo de estabilización tras el reset del Arduino
except Exception as e:
    print(f"[ERROR] No se pudo abrir el puerto: {e}")
    sys.exit(1)

# Asegurar la existencia del directorio de datos
os.makedirs("data", exist_ok=True)
archivo_csv = "data/registro_telemetria.csv"
f_csv = open(archivo_csv, "w", newline="", encoding="utf-8")
writer = csv.writer(f_csv)
writer.writerow(["Timestamp_ms", "Evento_ID", "Periodo_us", "Frecuencia_Hz", "RPM_Estimado"])
f_csv.flush()
print(f"[TELEMETRÍA] Registrando datos en: {archivo_csv}")

# Configuración de la interfaz gráfica
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))
fig.canvas.manager.set_window_title("INCIETEC 2026-2 | Telemetría Electromagnética BJT")
fig.subplots_adjust(hspace=0.35)

(line_hz,) = ax1.plot([], [], "b-o", markersize=4, lw=1.8, label="Frecuencia (Hz)")
ax1.set_title("Frecuencia de Perturbación Electromagnética (Ley de Faraday)", fontsize=11, fontweight="bold")
ax1.set_ylabel("Frecuencia [Hz]")
ax1.set_ylim(-0.5, 25.0)
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend(loc="upper left")

(line_rpm,) = ax2.plot([], [], "r-s", markersize=4, lw=1.8, label="Tacómetro (RPM)")
ax2.set_title("Velocidad Angular Estimada / Eventos por Minuto", fontsize=11, fontweight="bold")
ax2.set_xlabel("Tiempo Relativo [s]")
ax2.set_ylabel("Velocidad [RPM]")
ax2.set_ylim(-5.0, 1500.0)
ax2.grid(True, linestyle="--", alpha=0.6)
ax2.legend(loc="upper left")

tiempo_inicio = time.time()


def actualizar_grafica(frame):
    """Función de refresco ejecutada periódicamente por FuncAnimation."""
    while ser.in_waiting > 0:
        try:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea or "TIMESTAMP" in linea:
                continue

            partes = linea.split(",")
            if len(partes) == 5:
                t_ms = float(partes[0])
                ev_id = int(partes[1])
                per_us = float(partes[2])
                hz = float(partes[3])
                rpm = float(partes[4])

                # Guardar en CSV
                writer.writerow([t_ms, ev_id, per_us, hz, rpm])
                f_csv.flush()

                # Actualizar colas de visualización
                t_rel = time.time() - tiempo_inicio
                tiempos_s.append(t_rel)
                frecuencias_hz.append(hz)
                rpms.append(rpm)

        except (ValueError, IndexError):
            continue

    if tiempos_s:
        # Actualizar datos de las líneas
        line_hz.set_data(tiempos_s, frecuencias_hz)
        line_rpm.set_data(tiempos_s, rpms)

        # Ajuste dinámico de los límites en X
        min_x = max(0, tiempos_s[-1] - 15)
        max_x = tiempos_s[-1] + 1
        ax1.set_xlim(min_x, max_x)
        ax2.set_xlim(min_x, max_x)

        # Ajuste dinámico de Y si el valor supera la escala fija
        max_hz = max(max(frecuencias_hz, default=10), 10)
        ax1.set_ylim(-0.5, max_hz * 1.25)

        max_r = max(max(rpms, default=100), 100)
        ax2.set_ylim(-5.0, max_r * 1.25)

    return line_hz, line_rpm


ani = animation.FuncAnimation(fig, actualizar_grafica, interval=80, blit=False)

try:
    plt.show()
finally:
    ser.close()
    f_csv.close()
    print("[FINALIZADO] Puerto cerrado y datos guardados exitosamente.")