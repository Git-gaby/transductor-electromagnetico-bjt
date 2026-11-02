# Diagrama de Conexiones y Ruteo de Hardware

**Proyecto:** Sistema Híbrido de Sensado Electromagnético  
**Evento:** INCIETEC 2026-2  
**Plataforma de prueba:** Protoboard MB-102 (830 puntos)  

---

## 1. Distribución de Alimentación y Buses
* **Carril Rojo (+):** $V_{CC} = +5.0\text{ V}$ DC (suministrado por el módulo regulador HW-131).
* **Carril Azul (-):** $\text{GND}$ común para toda la electrónica analógica y el Arduino Nano.

> **Regla de oro:** Todos los terminales marcados como GND deben unirse al mismo bus negativo de la protoboard para asegurar una referencia de voltaje compartida.

---

## 2. Etapa de Sensado y Acondicionamiento (Bobina y Diodo)

1. **Bobina del relé desarmado:**
   * **Terminal 1:** Conectado directamente a la línea de tierra ($\text{GND}$).
   * **Terminal 2:** Conectado al **Ánodo** (patilla sin franja) del diodo rectificador **1N4007**.
2. **Diodo 1N4007:**
   * **Cátodo (extremo con la franja plateada/blanca):** Conectado al nodo de base del transistor $Q_1$.
3. **Resistencia de polarización (Pull-Down):**
   * Resistor de $100\text{ k}\Omega$ conectado entre el Cátodo del diodo (Base de $Q_1$) y $\text{GND}$. Fija el estado de corte en reposo.

---

## 3. Etapa de Amplificación y Conmutación BJT (Par en Cascada)

Para transistores NPN comunes en encapsulado TO-92 (**BC547**, **2N3904** o **S8050**), mirando la cara plana de frente con los pines hacia abajo:
* **BC547:** Pin 1 = Colector (C), Pin 2 = Base (B), Pin 3 = Emisor (E).
* **2N3904:** Pin 1 = Emisor (E), Pin 2 = Base (B), Pin 3 = Colector (C).

*(Verificar el datasheet específico según el modelo que venga en el kit).*

### Conexión del Transistor 1 ($Q_1$ - Preamplificador):
* **Base ($B_1$):** Conectada a la unión del Cátodo del diodo y la resistencia de pull-down.
* **Emisor ($E_1$):** Conectado a la Base ($B_2$) del segundo transistor ($Q_2$).
* **Colector ($C_1$):** Conectado al carril positivo ($+5.0\text{ V}$).

### Conexión del Transistor 2 ($Q_2$ - Driver de Salida / Conmutador):
* **Base ($B_2$):** Conectada al Emisor ($E_1$) del primer transistor.
* **Emisor ($E_2$):** Conectado directamente al carril de tierra ($\text{GND}$).
* **Colector ($C_2$):** Nodo de salida de señal. Aquí convergen tres elementos:
  1. El Cátodo del LED indicador.
  2. El pin de interrupción digital del Arduino Nano (**D2**).
  3. *(Opcional)* Sonda del multímetro / osciloscopio para verificación.

---

## 4. Indicador Óptico (Malla del LED)

1. **Resistencia de carga ($R_C = 220\ \Omega$):**
   * Un extremo conectado a $+5.0\text{ V}$.
   * El otro extremo conectado al **Ánodo** (patilla larga) del LED.
2. **Diodo LED (5 mm):**
   * **Ánodo (+):** Conectado a la resistencia $R_C$.
   * **Cátodo (-):** Patilla corta / chaflán plano conectado al Colector ($C_2$).

---

## 5. Acoplamiento de Telemetría (Arduino Nano)

| Pin Arduino Nano | Conexión en Protoboard | Función |
| :---: | :---: | :--- |
| **GND** | Carril Azul ($\text{GND}$) | Cierra el lazo de referencia común de 0V. |
| **D2 (INT0)** | Colector de $Q_2$ ($C_2$) | Captura el flanco de bajada ($5\text{ V} \rightarrow 0.2\text{ V}$) por interrupción externa. |
| **VIN / 5V** | *(No conectar)* | El Arduino se alimenta directamente por el cable USB desde la PC. |

---

## 6. Diagrama de Flujo de Señal

```text
[Imán de Neodimio] (Movimiento dΦ/dt)
       │
       ▼
 [Bobina de Relé] ──► Genera pulso FEM inducida
       │
       ▼
 [Diodo 1N4007]   ──► Rectifica pulso positivo y protege BJT
       │
       ▼
 [Base Q1 (BC547)]──► Amplifica corriente transitoria
       │
       ▼
 [Base Q2 (BC547)]──► Entra en saturación (Vce ≈ 0.2V)
       │
       ├───► [Cátodo LED] ──────► Enciende indicador luminoso
       │
       └───► [Pin D2 Arduino] ──► Dispara ISR externa -> Telemetría USB