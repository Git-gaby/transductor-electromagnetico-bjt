# Lista de Materiales (Bill of Materials - BOM)

## Proyecto: Transductor de Inducción Electromagnética y Conmutación BJT
**Evento:** INCIETEC 2026-2  
**Modalidad:** Prototipo Experimental  

---

### 1. Componentes Físicos y Transductores

| Ítem | Componente / Descripción | Cantidad | Referencia / Especificación | Función en el Sistema |
| :--- | :--- | :---: | :--- | :--- |
| 1 | **Solenoide sensor (Bobina)** | 1 | Bobina desacoplada de relé electromecánico (5V o 12V DC) | Transductor primario: convierte la variación de flujo magnético en FEM inducida (Ley de Faraday). |
| 2 | **Dipolo magnético móvil** | 1 o 2 | Imán permanente de Neodimio (NdFeB), grado N35 o superior | Generador del campo magnético estático móvil ($B$). |

---

### 2. Etapa Electrónica Analógica y Acondicionamiento

| Ítem | Componente / Descripción | Cantidad | Referencia / Especificación | Función en el Sistema |
| :--- | :--- | :---: | :--- | :--- |
| 3 | **Diodo rectificador rápido / propósito general** | 1 | 1N4007 (o 1N4148) | Rectificación de media onda: bloquea semiciclos negativos y protege la unión base-emisor del BJT. |
| 4 | **Transistores de Unión Bipolar (BJT)** | 2 | NPN BC547B (o 2N3904 / S8050) | Etapa de amplificación en cascada y conmutación corte/saturación. |
| 5 | **Resistencia de polarización de base** | 1 | Resistor $100\text{ k}\Omega$ a $1\text{ M}\Omega$ (1/4 W, $\pm 5\%$) | Resistencia de drenaje a tierra (pull-down) para fijar el corte en ausencia de perturbación. |
| 6 | **Resistencia limitadora de colector** | 1 | Resistor $220\ \Omega$ o $330\ \Omega$ (1/4 W, $\pm 5\%$) | Protección del LED y fijación de corriente de colector ($I_C \approx 12.7\text{ mA}$) a 5V. |
| 7 | **Diodo Emisor de Luz (LED)** | 1 | LED estándar 5 mm (Rojo o Verde, $V_F \approx 2.0\text{ V}$) | Indicador óptico de conmutación de estado en tiempo real. |

---

### 3. Instrumentación Digital y Adquisición de Datos

| Ítem | Componente / Descripción | Cantidad | Referencia / Especificación | Función en el Sistema |
| :--- | :--- | :---: | :--- | :--- |
| 8 | **Placa de microcontrolador** | 1 | Arduino Nano V3.0 (ATmega328P, chip USB CH340) | Muestreo digital mediante interrupciones de hardware (Pin D2) y transmisión serial UART. |
| 9 | **Cable de interfaz de datos** | 1 | Cable USB a Mini-USB (apantallado) | Enlace de telemetría bidireccional hacia la computadora y alimentación digital. |

---

### 4. Soporte, Conexión y Alimentación

| Ítem | Componente / Descripción | Cantidad | Referencia / Especificación | Función en el Sistema |
| :--- | :--- | :---: | :--- | :--- |
| 10 | **Tablero de pruebas (Protoboard)** | 1 | MB-102 (830 puntos) | Plataforma de inserción sin soldadura para ensamble modular. |
| 11 | **Cables jumpers de interconexión** | 1 juego | Cables rígidos tipo U / cables dupont macho-macho | Ruteo de señales, líneas de bus y tierras comunes. |
| 12 | **Módulo de alimentación regulada** | 1 | Módulo HW-131 para protoboard | Suministro de carril regulado de 5.0V DC limpios. |