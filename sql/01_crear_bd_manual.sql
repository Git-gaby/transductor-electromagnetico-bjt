-- INCIETEC - Base de datos de sensado electromagnetico manual
-- Usar solo para una instalacion nueva (MySQL 8.0+).
-- No borra datos existentes. Si ya utilizaste la base anterior,
-- utiliza 02_actualizar_bd_existente.sql despues de respaldarla.

CREATE DATABASE IF NOT EXISTS sensado_electromagnetico
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sensado_electromagnetico;

-- Un ensayo corresponde a una sesion de prueba manual con el iman.
CREATE TABLE IF NOT EXISTS ensayos (
    id_ensayo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(255),
    observaciones TEXT
);

-- Una medicion corresponde a una muestra de telemetria del Arduino.
CREATE TABLE IF NOT EXISTS mediciones (
    id_medicion BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_ensayo INT NOT NULL,
    timestamp_ms BIGINT UNSIGNED NOT NULL,
    conteo_eventos BIGINT UNSIGNED NOT NULL,
    intervalo_s DECIMAL(14,6) NULL,
    frecuencia_hz DECIMAL(12,3) NOT NULL DEFAULT 0,
    estado_logico ENUM('HIGH', 'LOW') NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_mediciones_ensayos FOREIGN KEY (id_ensayo)
        REFERENCES ensayos(id_ensayo),
    CONSTRAINT uq_ensayo_timestamp UNIQUE (id_ensayo, timestamp_ms),
    CONSTRAINT chk_intervalo_no_negativo CHECK
        (intervalo_s IS NULL OR intervalo_s >= 0),
    CONSTRAINT chk_frecuencia_no_negativa CHECK (frecuencia_hz >= 0)
);

-- AVG calcula la media de muestras con frecuencia positiva.
-- MAX(conteo_eventos) refleja el contador maximo de flancos de cada ensayo
-- si el Arduino no se reinicia durante ese ensayo.
CREATE OR REPLACE VIEW resumen_ensayos AS
SELECT
    e.id_ensayo,
    e.nombre,
    e.fecha_inicio,
    COUNT(m.id_medicion) AS total_muestras,
    COALESCE(MAX(m.conteo_eventos), 0) AS eventos_contados,
    ROUND(AVG(CASE WHEN m.frecuencia_hz > 0 THEN m.frecuencia_hz END), 2)
        AS frecuencia_promedio_hz,
    ROUND(MAX(m.frecuencia_hz), 2) AS frecuencia_maxima_hz,
    SUM(CASE WHEN m.estado_logico = 'LOW' THEN 1 ELSE 0 END)
        AS muestras_estado_low
FROM ensayos e
LEFT JOIN mediciones m ON e.id_ensayo = m.id_ensayo
GROUP BY e.id_ensayo, e.nombre, e.fecha_inicio;
