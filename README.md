# Sistema Híbrido de Sensado Electromagnético (INCIETEC 2026-2)

**Modalidad:** Prototipo Experimental  
**Categoría:** Junior (1° - 4° Semestre)  
**Institución:** Corporación Universitaria Unilasallista  
**Asignaturas:** Física de Campos & Circuitos / Dispositivos Semiconductores  

---

## 📌 Descripción del Proyecto
Prototipo experimental que integra la transducción electromagnética basada en la Ley de Faraday-Lenz con una etapa de conmutación en estado sólido mediante transistores BJT NPN. El circuito sensa perturbaciones de campo magnético producidas por un imán de neodimio, amplifica la corriente inducida para saturar el transistor y encender un LED, y transmite los eventos de conmutación a un microcontrolador Arduino Nano para telemetría y graficación de métricas en tiempo real.

## 🔬 Fundamentación Teórica
- **Física de Campos:** Inducción electromagnética ($\varepsilon = -N \frac{d\Phi_B}{dt}$), Ley de Lenz y dipolos magnéticos.
- **Circuitos Electrónicos:** Polarización de transistores BJT, ganancia de corriente ($\beta$), cálculo de mallas mediante Leyes de Kirchhoff y conmutación corte/saturación.
- **Sistemas Embebidos:** Detección de flancos por interrupciones de hardware y comunicación serial UART a 115200 baudios.

## 🛠️ Componentes Principales
- Solenoide ferromagnético (bobina de relé desacoplada)
- Imán permanente de neodimio
- Diodo rectificador 1N4007
- Transistores NPN (BC547 / 2N3904)
- Microcontrolador Arduino Nano (ATmega328P)
- Módulo de alimentación MB-102 (5V DC) y LED indicador

---
*Proyecto en desarrollo para la sustentación presencial en la semana de INCIETEC (Noviembre 2026).*