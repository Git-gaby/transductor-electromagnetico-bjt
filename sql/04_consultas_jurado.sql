USE sensado_electromagnetico;

-- Ultimas 15 muestras (estado es un muestreo, no cada pulso).
SELECT * FROM mediciones ORDER BY id_medicion DESC LIMIT 15;

-- Resumen de todos los ensayos manuales.
SELECT * FROM resumen_ensayos ORDER BY id_ensayo DESC;

-- Estadisticas basicas por ensayo. No confundir muestras con eventos.
SELECT id_ensayo,
       COUNT(*) AS total_muestras,
       MAX(conteo_eventos) AS eventos_contados,
       ROUND(AVG(CASE WHEN frecuencia_hz > 0 THEN frecuencia_hz END), 2)
           AS frecuencia_promedio_hz,
       MAX(frecuencia_hz) AS frecuencia_maxima_hz,
       MIN(CASE WHEN frecuencia_hz > 0 THEN frecuencia_hz END)
           AS frecuencia_minima_positiva_hz
FROM mediciones
GROUP BY id_ensayo;




SELECT * FROM mediciones WHERE frecuencia_hz > 0 ORDER BY id_medicion DESC LIMIT 30;

SELECT * FROM mediciones ORDER BY id_medicion DESC LIMIT 15;