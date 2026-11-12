-- INCIETEC - MIGRACION desde el esquema anterior de este proyecto.
-- IMPORTANTE: ejecutar UNA SOLA VEZ, despues de hacer respaldo.
-- Conserva ensayos y mediciones previas; NO inventa estados HIGH/LOW.
-- Las mediciones antiguas quedan con estado_logico = NULL.
-- Requiere que existan columnas: tipo_movimiento, evento_id, periodo_us,
-- rpm_estimado. No usar sobre una instalacion nueva ni repetir.

USE sensado_electromagnetico;

DROP VIEW IF EXISTS resumen_ensayos;

-- El CHECK del esquema viejo impide borrar rpm_estimado si no se elimina.
ALTER TABLE mediciones DROP CHECK chk_rpm_no_negativa;

ALTER TABLE mediciones
    ADD COLUMN intervalo_s DECIMAL(14,6) NULL AFTER periodo_us,
    ADD COLUMN estado_logico ENUM('HIGH', 'LOW') NULL AFTER frecuencia_hz;

-- El firmware anterior enviaba microsegundos: s = us / 1000000.
-- Para periodo_us = 0 no existe todavia un intervalo valido.
UPDATE mediciones
SET intervalo_s = CASE
    WHEN periodo_us = 0 THEN NULL
    ELSE ROUND(periodo_us / 1000000.0, 6)
END;

ALTER TABLE mediciones
    CHANGE COLUMN evento_id conteo_eventos BIGINT UNSIGNED NOT NULL,
    DROP COLUMN periodo_us,
    DROP COLUMN rpm_estimado;

-- Todos los ensayos son manuales; esa categoria deja de ser necesaria.
ALTER TABLE ensayos
    DROP COLUMN tipo_movimiento;

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
