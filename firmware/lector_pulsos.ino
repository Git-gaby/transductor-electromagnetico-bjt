/*
 * INCIETEC - Arduino Nano clasico (ATmega328P)
 * Conteo de eventos manuales, tiempo de muestra, intervalo y frecuencia.
 * Estado HIGH/LOW = nivel logico leido al ENVIAR cada muestra (cada 100 ms).
 * No registra todos los transitorios LOW si los pulsos son muy cortos.
 * El conteo por interrupciones es la evidencia principal de eventos.
 * Conexion: colector de salida BJT -> D2; tierras comunes.
 */
const byte PIN_SENSOR = 2;  // interrupcion INT0
volatile unsigned long conteoEventos = 0;
volatile unsigned long ultimoEventoUs = 0;
volatile unsigned long intervaloUs = 0;

unsigned long ultimaMuestraMs = 0;
const unsigned long INTERVALO_MUESTRA_MS = 100;

void detectarPulso() {
  unsigned long ahora = micros();
  // Aceptar el primer pulso o uno separado por mas de 5 ms.
  if (ultimoEventoUs == 0 || (unsigned long)(ahora - ultimoEventoUs) > 5000UL) {
    // El primer pulso no tiene un intervalo valido previo.
    intervaloUs = (ultimoEventoUs == 0) ? 0 : ahora - ultimoEventoUs;
    ultimoEventoUs = ahora;
    conteoEventos++;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_SENSOR, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_SENSOR), detectarPulso, FALLING);
  Serial.println("TIMESTAMP_MS,CONTEO_EVENTOS,INTERVALO_S,FRECUENCIA_HZ,ESTADO_LOGICO");
}

void loop() {
  unsigned long ahoraMs = millis();
  if ((unsigned long)(ahoraMs - ultimaMuestraMs) < INTERVALO_MUESTRA_MS) return;
  ultimaMuestraMs = ahoraMs;

  noInterrupts();
  unsigned long conteo = conteoEventos;
  unsigned long deltaUs = intervaloUs;
  unsigned long ultimoUs = ultimoEventoUs;
  interrupts();

  // Si han pasado mas de 2 segundos sin pulso, frecuencia = 0.
  float frecuencia = 0.0;
  if (deltaUs > 0 && ultimoUs > 0 &&
      (unsigned long)(micros() - ultimoUs) < 2000000UL) {
    frecuencia = 1000000.0 / (float)deltaUs;
  }

  // Estado INSTANTANEO durante el muestreo, no estado en cada flanco.
  const char* estado = (digitalRead(PIN_SENSOR) == LOW) ? "LOW" : "HIGH";

  Serial.print(ahoraMs);
  Serial.print(',');
  Serial.print(conteo);
  Serial.print(',');
  Serial.print(deltaUs / 1000000.0, 6);
  Serial.print(',');
  Serial.print(frecuencia, 3);
  Serial.print(',');
  Serial.println(estado);
}
