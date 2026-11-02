# Memoria Técnica y Fundamentación Teórica

**Proyecto:** Sistema Híbrido de Sensado Electromagnético  
**Evento:** Jornada Académica INCIETEC 2026-2  
**Modalidad:** Prototipo Experimental  
**Categoría:** Junior (1° - 4° Semestre)  
**Autor:** Gabriel Jaime Gómez Restrepo  

---

## 1. Fundamentación en Física de Campos

### 1.1 Ley de Inducción de Faraday y Ley de Lenz
El principio de operación del transductor primario se fundamenta en la variación temporal del flujo magnético ($\Phi_B$) a través de una superficie delimitada por un circuito cerrado. De acuerdo con la **Ley de Faraday**:

$$\varepsilon = -\frac{d\Phi_B}{dt}$$

Para un solenoide conformado por $N$ espiras devanadas sobre un núcleo ferromagnético de permeabilidad magnética $\mu$, la fuerza electromotriz (FEM) inducida total se escala de manera proporcional al número de vueltas:

$$\varepsilon_{\text{total}} = -N \frac{d}{dt} \int_{S} \vec{B} \cdot d\vec{A}$$

El signo negativo impuesto por la **Ley de Lenz** establece que la corriente inducida genera un campo magnético secundario $\vec{B}_{\text{ind}}$ que se opone diametralmente a la variación del flujo que lo produjo, asegurando el principio de conservación de la energía.

### 1.2 Dinámica del Dipolo Magnético Móvil
El campo magnético generado por un imán permanente de neodimio (NdFeB) a lo largo de su eje axial $z$ se modela analíticamente como un dipolo magnético de momento dipolar $\vec{m}$:

$$B_z(z) = \frac{\mu_0}{4\pi} \frac{2m}{z^3}$$

Cuando el imán se aproxima hacia el solenoide a una velocidad instantánea $v_z = \frac{dz}{dt}$, la tasa temporal de cambio del gradiente de campo magnético es:

$$\frac{dB_z}{dt} = \frac{dB_z}{dz} \frac{dz}{dt} = \left(-\frac{3\mu_0 m}{2\pi z^4}\right) v_z$$

Por consiguiente, la magnitud del voltaje pico inducido $\varepsilon_p$ depende críticamente de dos factores experimentales:
1. **La velocidad relativa ($v_z$):** A mayor velocidad de desplazamiento del imán, mayor es $\frac{d\Phi_B}{dt}$ y mayor la FEM inducida.
2. **La distancia axial ($z$):** La intensidad de acoplamiento decae con una dependencia geométrica inversamente proporcional a la cuarta potencia de la distancia respecto al solenoide.

---

## 2. Fundamentación en Circuitos y Dispositivos Semiconductores

### 2.1 Acondicionamiento y Protección de Entrada (Juntura p-n)
La oscilación del dipolo produce una señal alterna (AC) transitoria:
- Durante la aproximación del dipolo: $\varepsilon > 0$ (polaridad directa hacia la base del transistor).
- Durante el alejamiento del dipolo: $\varepsilon < 0$ (polaridad inversa).

Los transistores BJT NPN poseen un voltaje de ruptura inverso base-emisor muy bajo ($V_{EBO} \approx 6.0\text{ V}$). Para proteger la juntura semiconductora frente a picos inductivos inversos de alta tensión (regidos por $V = -L \frac{di}{dt}$), se incorpora un **diodo rectificador 1N4007** en serie con la bobina, bloqueando los semiciclos negativos y rectificando la señal a media onda.

### 2.2 Conmutación y Región de Saturación en Transistores BJT
La corriente inducida rectificada $i_{\text{ind}}(t)$ se inyecta en la base del primer transistor ($Q_1$). La red multietapa opera como conmutador de estado sólido:

* **Estado de Reposo (Corte):** En ausencia de variación de flujo magnético ($\frac{d\Phi_B}{dt} = 0$):
  $$I_B \approx 0 \implies V_{BE} < 0.65\text{ V} \implies I_C \approx 0$$
  El transistor actúa como un interruptor abierto; el LED se encuentra apagado y la tensión de colector se mantiene en nivel alto ($V_{CE} \approx V_{CC} = 5.0\text{ V}$).

* **Estado de Excitación (Saturación):** Al inducirse la corriente de base suficiente:
  $$I_B \ge \frac{I_{C(\text{sat})}}{\beta_{\text{total}}}$$
  La juntura colector-base se polariza en directa, forzando la transición a saturación:
  $$V_{CE(\text{sat})} \approx 0.2\text{ V}$$
  El transistor actúa como un interruptor cerrado ideal, derivando la corriente de colector hacia tierra (GND) y cerrando la malla del LED.

### 2.3 Análisis de Mallas mediante Ley de Voltajes de Kirchhoff (LVK)
Para la malla de salida con el transistor saturado y la fuente de alimentación regulada a $V_{CC} = 5.0\text{ V}$ DC:

$$V_{CC} - I_C R_C - V_{\text{LED}} - V_{CE(\text{sat})} = 0$$

Despejando la corriente nominal que atraviesa el indicador óptico:

$$I_C = \frac{V_{CC} - V_{\text{LED}} - V_{CE(\text{sat})}}{R_C}$$

Sustituyendo los parámetros nominales del circuito:
- $V_{CC} = 5.0\text{ V}$ (suministrados por módulo HW-131)
- $V_{\text{LED}} \approx 2.0\text{ V}$ (LED rojo estándar de 5 mm)
- $V_{CE(\text{sat})} \approx 0.2\text{ V}$ (BC547B en saturación profunda)
- $R_C = 220\ \Omega$ (resistor de 1/4 W)

$$I_C = \frac{5.0\text{ V} - 2.0\text{ V} - 0.2\text{ V}}{220\ \Omega} = \frac{2.8\text{ V}}{220\ \Omega} \approx 12.72\text{ mA}$$

**Comprobación de disipación de potencia en el resistor:**
$$P_{R_C} = I_C^2 \cdot R_C = (12.72\text{ mA})^2 \cdot 220\ \Omega \approx 35.6\text{ mW} \ll 250\text{ mW}$$
El componente opera dentro de los límites térmicos nominales con un factor de seguridad superior a 7.

---

## 3. Capa Digital: Detección por Interrupciones y Telemetría

### 3.1 Captura Asíncrona (Hardware Interrupts)
El microcontrolador ATmega328P (Arduino Nano) monitoriza el colector del transistor mediante el pin de interrupción externa **INT0 (D2)**.
- Cuando el BJT conmuta a saturación, la línea cae de $5\text{ V}$ a $0.2\text{ V}$, produciendo un flanco de bajada (**FALLING edge**).
- La Rutina de Servicio de Interrupción (`ISR`) captura la marca temporal precisa en microsegundos mediante el temporizador interno por hardware:
  $$\Delta t = t_k - t_{k-1}$$
  $$f_{\text{instantánea}} = \frac{10^6}{\Delta t} \quad [\text{Hz}]$$
  $$\text{RPM} = f_{\text{instantánea}} \times 60$$

### 3.2 Transmisión y Registro
Las métricas procesadas se transmiten vía UART hacia la interfaz gráfica en Python a una tasa de transferencia de $115200\text{ baudios}$, garantizando una latencia inferior a $10\text{ ms}$ y permitiendo la visualización fluida de métricas en tiempo real.