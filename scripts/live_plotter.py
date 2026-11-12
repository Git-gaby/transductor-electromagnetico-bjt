"""INCIETEC: Arduino Nano -> Python -> MySQL + CSV + graficas.

Requiere el firmware lector_pulsos_manual_mysql.ino de este paquete.
Formato: TIMESTAMP_MS,CONTEO_EVENTOS,INTERVALO_S,FRECUENCIA_HZ,ESTADO_LOGICO
Este codigo usa Visual Studio o Visual Studio Code en Windows.
"""
import csv
import math
import sys
import time
from collections import deque
from datetime import datetime
from getpass import getpass
from pathlib import Path

import mysql.connector
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Si la deteccion falla, indica el COM real. Ejemplo: "COM3".
PUERTO_MANUAL = None
BAUDIOS = 115200
ULTIMAS_MUESTRAS = 60


def detectar_puerto():
    if PUERTO_MANUAL:
        return PUERTO_MANUAL
    candidatos = list(serial.tools.list_ports.comports())
    for p in candidatos:
        desc = p.description.lower()
        if any(x in desc for x in ("arduino", "ch340", "usb-serial", "usb serial")):
            return p.device
    return candidatos[0].device if len(candidatos) == 1 else None


def leer_muestra(linea):
    """Convierte el CSV del NUEVO firmware a valores para MySQL."""
    partes = [p.strip() for p in linea.split(",")]
    if len(partes) != 5:
        return None
    try:
        t_ms = int(partes[0])
        conteo = int(partes[1])
        delta = float(partes[2])
        hz = float(partes[3])
        estado = partes[4].upper()
    except ValueError:
        return None
    if (t_ms < 0 or conteo < 0 or delta < 0 or hz < 0
            or not math.isfinite(delta) or not math.isfinite(hz)
            or estado not in ("HIGH", "LOW")):
        return None
    # Antes de dos pulsos no hay intervalo valido.
    intervalo = round(delta, 6) if conteo >= 2 and delta > 0 else None
    return t_ms, conteo, intervalo, round(hz, 3), estado


def main():
    puerto = detectar_puerto()
    if not puerto:
        print("[ERROR] Arduino no detectado. Revisa USB o configura PUERTO_MANUAL.")
        sys.exit(1)

    # Abrir serial primero: confirmar el Arduino antes de crear un ensayo.
    try:
        arduino = serial.Serial(puerto, BAUDIOS, timeout=0.1)
        time.sleep(2)  # Arduino Nano puede reiniciarse al abrir el puerto.
        print(f"[OK] Arduino en {puerto} a {BAUDIOS} baudios")
    except serial.SerialException as exc:
        print(f"[ERROR SERIAL] {exc}")
        sys.exit(1)

    try:
        db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password=getpass("Contrasena local de MySQL: "),
            database="sensado_electromagnetico",
        )
    except mysql.connector.Error as exc:
        arduino.close()
        print(f"[ERROR MYSQL] {exc}")
        sys.exit(1)

    cursor = db.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute(
            "INSERT INTO ensayos (nombre, descripcion) VALUES (%s, %s)",
            (f"Ensayo manual {fecha}", "Movimiento manual del iman sobre la bobina"),
        )
        db.commit()
    except mysql.connector.Error as exc:
        print(f"[ERROR CREANDO ENSAYO] {exc}")
        cursor.close()
        db.close()
        arduino.close()
        sys.exit(1)
    id_ensayo = cursor.lastrowid
    print(f"[OK] Ensayo manual numero {id_ensayo}")

    # Guardar respaldo CSV sin sobrescribir sesiones previas.
    carpeta = Path(__file__).resolve().parent.parent / "data"
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / ("manual_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv")
    archivo = ruta.open("w", newline="", encoding="utf-8")
    writer = csv.writer(archivo)
    writer.writerow(["timestamp_ms", "conteo_eventos", "intervalo_s",
                     "frecuencia_hz", "estado_logico"])
    archivo.flush()

    tiempos = deque(maxlen=ULTIMAS_MUESTRAS)
    frecs = deque(maxlen=ULTIMAS_MUESTRAS)
    conteos = deque(maxlen=ULTIMAS_MUESTRAS)
    fig, (ax_hz, ax_c) = plt.subplots(2, 1, figsize=(9, 6))
    fig.subplots_adjust(hspace=0.45)
    linea_hz, = ax_hz.plot([], [], marker="o", markersize=3)
    linea_c, = ax_c.plot([], [], marker="o", markersize=3)
    ax_hz.set(title="Frecuencia de paso manual", ylabel="Frecuencia (Hz)")
    ax_c.set(title="Conteo acumulado de eventos", xlabel="Tiempo (s)",
             ylabel="Eventos")
    ax_hz.grid(True)
    ax_c.grid(True)
    aviso_formato = False
    total_guardadas = 0

    def actualizar(_frame):
        nonlocal aviso_formato, total_guardadas
        while arduino.in_waiting:
            texto = arduino.readline().decode("utf-8", errors="ignore").strip()
            if not texto:
                continue
            if texto.upper().startswith("TIMESTAMP"):
                if "RPM" in texto.upper() and not aviso_formato:
                    print("[AVISO] Firmware anterior detectado (envia RPM). "
                          "Carga lector_pulsos_manual_mysql.ino.")
                    aviso_formato = True
                continue
            muestra = leer_muestra(texto)
            if muestra is None:
                if not aviso_formato:
                    print("[AVISO] Linea incompatible. Se requiere el firmware "
                          "nuevo con estado HIGH/LOW.")
                    aviso_formato = True
                continue

            t_ms, conteo, intervalo, hz, estado = muestra
            writer.writerow([t_ms, conteo, "" if intervalo is None else intervalo,
                             hz, estado])
            archivo.flush()
            try:
                cursor.execute(
                    "INSERT INTO mediciones "
                    "(id_ensayo, timestamp_ms, conteo_eventos, intervalo_s, "
                    "frecuencia_hz, estado_logico) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_ensayo, t_ms, conteo, intervalo, hz, estado),
                )
                db.commit()
                total_guardadas += 1
            except mysql.connector.Error as exc:
                db.rollback()
                print(f"[ERROR GUARDANDO] {exc}")

            tiempos.append(t_ms / 1000.0)
            frecs.append(hz)
            conteos.append(conteo)

        if tiempos:
            linea_hz.set_data(tiempos, frecs)
            linea_c.set_data(tiempos, conteos)
            xmin = max(0, tiempos[-1] - 15)
            xmax = tiempos[-1] + 1
            for eje in (ax_hz, ax_c):
                eje.set_xlim(xmin, xmax)
            ax_hz.set_ylim(-0.5, max(1, max(frecs)) * 1.25)
            ax_c.set_ylim(-0.5, max(1, max(conteos)) * 1.25)
        return linea_hz, linea_c

    animacion = FuncAnimation(fig, actualizar, interval=100,
                              cache_frame_data=False)
    try:
        plt.show()
    finally:
        # Conservar una referencia a animacion evita eliminacion temprana.
        _ = animacion
        archivo.close()
        arduino.close()
        cursor.close()
        db.close()
        print(f"[FIN] {total_guardadas} muestras insertadas. CSV: {ruta}")


if __name__ == "__main__":
    main()
