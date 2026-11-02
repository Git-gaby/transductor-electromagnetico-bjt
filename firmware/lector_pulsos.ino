/**
 * @file lector_pulsos.ino
 * @brief Adquisición de eventos de conmutación electromagnética vía interrupciones.
 * @project Sistema Híbrido de Sensado Electromagnético (INCIETEC 2026-2)
 * @author Gabriel Jaime Gómez Restrepo
 * 
 * Conexión física:
 * - Colector del transistor BJT de salida -> Pin D2 (INT0) del Arduino Nano.
 * - GND del circuito analógico -> Pin GND del Arduino Nano (Tierra común obligatoria).
 */

const byte PIN_SENSOR = 2; // Pin D2 cuenta con soporte de interrupción externa (INT0)

// Variables compartidas con la Rutina de Servicio de Interrupción (ISR)
volatile unsigned long conteoPulsos = 0;
volatile unsigned long ultimoTiempoMicros = 0;
volatile unsigned long periodoMicros = 0;
volatile bool nuevoEvento = false;

// Variables para el control de telemetría en el loop principal
unsigned long tiempoPrevioSerial = 0;
const unsigned long INTERVALO_SERIAL_MS = 100; // Envío de telemetría cada 100 ms

/**
 * @brief Rutina de Servicio de Interrupción (ISR)
 * Se ejecuta de forma asíncrona ante cada flanco de bajada (FALLING) en el colector.
 */
void ICACHE_RAM_ATTR sensorISR() {
  unsigned long tiempoActual = micros();
  // Filtro anti-rebote por software para evitar falsos disparos por ruido inductivo (> 5 ms)
  if (tiempoActual - ultimoTiempoMicros > 5000) {
    periodoMicros = tiempoActual - ultimoTiempoMicros;
    ultimoTiempoMicros = tiempoActual;
    conteoPulsos++;
    nuevoEvento = true;
  }
}

void setup() {
  // Configuración de la tasa de baudios para transmisión rápida
  Serial.begin(115200);

  // Configuración del pin de entrada con resistencia pull-up interna activa
  pinMode(PIN_SENSOR, INPUT_PULLUP);

  // Vinculación de la interrupción: dispara cuando el BJT satura y lleva la línea a GND
  attachInterrupt(digitalPinToInterrupt(PIN_SENSOR), sensorISR, FALLING);

  // Encabezado de telemetría para el script de procesamiento en Python
  Serial.println("TIMESTAMP_MS,EVENTO_ID,PERIODO_US,FRECUENCIA_HZ,RPM_ESTIMADO");
}

void loop() {
  unsigned long tiempoActualMs = millis();

  // Envío periódico de métricas por el puerto serial
  if (tiempoActualMs - tiempoPrevioSerial >= INTERVALO_SERIAL_MS) {
    tiempoPrevioSerial = tiempoActualMs;

    float frecuenciaHz = 0.0;
    float rpm = 0.0;

    // Sección crítica: lectura de variables atómicas modificadas por la ISR
    noInterrupts();
    unsigned long periodoLocal = periodoMicros;
    unsigned long conteoLocal = conteoPulsos;
    bool eventoLocal = nuevoEvento;
    nuevoEvento = false;
    interrupts();

    // Si hubo un pulso reciente en los últimos 2 segundos, calculamos la dinámica
    if ((micros() - ultimoTiempoMicros) < 2000000 && periodoLocal > 0) {
      frecuenciaHz = 1000000.0 / (float)periodoLocal;
      rpm = frecuenciaHz * 60.0;
    }

    // Trama de datos en formato CSV: tiempo, conteo, periodo, Hz, RPM
    Serial.print(tiempoActualMs);
    Serial.print(",");
    Serial.print(conteoLocal);
    Serial.print(",");
    Serial.print(periodoLocal);
    Serial.print(",");
    Serial.print(frecuenciaHz, 2);
    Serial.print(",");
    Serial.println(rpm, 1);
  }
}