-- PRUEBA OPCIONAL de la estructura SIN Arduino.
-- TODOS LOS DATOS SIGUIENTES SON SIMULADOS.
-- No presentar estos resultados como datos del experimento real.
USE sensado_electromagnetico;

INSERT INTO ensayos (nombre, descripcion)
VALUES ('SIMULADO - Verificacion de SQL', 'Datos ficticios para probar consultas');
SET @id_ensayo_prueba = LAST_INSERT_ID();

INSERT INTO mediciones
(id_ensayo, timestamp_ms, conteo_eventos, intervalo_s, frecuencia_hz, estado_logico)
VALUES
(@id_ensayo_prueba, 1000, 0, NULL, 0.000, 'HIGH'),
(@id_ensayo_prueba, 1100, 1, NULL, 0.000, 'LOW'),
(@id_ensayo_prueba, 1200, 1, NULL, 0.000, 'HIGH'),
(@id_ensayo_prueba, 1300, 2, 0.200000, 5.000, 'LOW'),
(@id_ensayo_prueba, 1400, 2, 0.200000, 5.000, 'HIGH'),
(@id_ensayo_prueba, 1500, 3, 0.100000, 10.000, 'HIGH');

SELECT * FROM mediciones WHERE id_ensayo = @id_ensayo_prueba;
SELECT * FROM resumen_ensayos WHERE id_ensayo = @id_ensayo_prueba;
