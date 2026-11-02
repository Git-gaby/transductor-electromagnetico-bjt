# Sistema Híbrido de Sensado Electromagnético

**Evento:** Jornada Académica INCIETEC 2026-2  
**Institución:** Corporación Universitaria Unilasallista  
**Modalidad:** Prototipo Experimental (Categoría Junior)  
**Autor:** Gabriel Jaime Gómez Restrepo  
**Asignaturas Vinculadas:** Física de Campos & Circuitos / Dispositivos Semiconductores  

---

## 📌 Resumen del Proyecto

Este prototipo experimental desarrolla un sistema de detección e instrumentación física que articula la **inducción electromagnética (Faraday-Lenz)** con la **electrónica de conmutación en estado sólido (transistores BJT NPN)** y la **telemetría digital en tiempo real**.

El transductor primario (bobina de relé desacoplada con núcleo ferromagnético) detecta la perturbación del flujo magnético provocada por un imán de neodimio móvil. La fuerza electromotriz (FEM) inducida es rectificada mediante una unión p-n (diodo 1N4007) y acondiciona la base de una etapa de transistores BJT para conmutar entre corte y saturación ($V_{CE} \approx 0.2\text{ V}$), activando un indicador LED. 

Para dotar al proyecto de carácter cuantitativo e investigativo, la salida del conmutador se conecta a un microcontrolador **Arduino Nano**, el cual captura los eventos mediante interrupciones por hardware y transmite la telemetría a un script en Python para graficar frecuencia (Hz) y velocidad angular equivalente (RPM) en tiempo real.

---

## 🧭 Estructura del Repositorio

El repositorio se organiza bajo la siguiente arquitectura modular:

* 📄 **[hardware/BOM_materiales.md](hardware/BOM_materiales.md):** Lista de materiales detallada con tolerancias, referencias comerciales y funciones en el circuito.
* 📄 **[hardware/esquematico.md](hardware/esquematico.md):** Guía de conexión pin a pin en protoboard y distribución de buses de alimentación.
* 💻 **[firmware/lector_pulsos.ino](firmware/lector_pulsos.ino):** Código en C++ para Arduino Nano con captura por interrupciones externas (Pin D2 / INT0).
* 🐍 **[scripts/live_plotter.py](scripts/live_plotter.py):** Aplicación en Python para lectura del puerto serial, exportación a CSV y graficación dinámica en vivo.
* 📐 **[docs/memoria_tecnica.md](docs/memoria_tecnica.md):** Sustentación matemática completa (Ley de Faraday, dipolo magnético, mallas LVK y región de saturación).

---

## 🚀 Requisitos para la Demostración

1. **Hardware:**
   * Circuito analógico montado en protoboard alimentado a $5.0\text{ V}$ DC.
   * Arduino Nano conectado vía USB al PC (GND común con la protoboard y pin D2 al colector de salida).
2. **Software:**
   * Python 3.9+ instalado en el equipo.
   * Dependencias de telemetría:
     ```bash
     pip install pyserial matplotlib
     ```
   * Ejecución de la interfaz:
     ```bash
     python scripts/live_plotter.py
     ```

---
*Desarrollado para la presentación oficial en la muestra de prototipos de INCIETEC 2026-2.*