-- ============================================================================
-- Capítulo 7 · Figura 7.6 — Un interbloqueo en los registros del motor
--
-- Dos consultas de apoyo:
--   (a) La vista de "quién espera a quién" (pg_blocking_pids), para VER el
--       bloqueo en vivo mientras el script 7_6_interbloqueo.py está trabado.
--   (b) La configuración de log_lock_waits + deadlock_timeout, para que
--       PostgreSQL anote el interbloqueo en su registro (lo que muestra la
--       Figura 7.6: qué dos transacciones, qué recursos, cuál fue la víctima).
-- ============================================================================

-- ---------------------------------------------------------------------------
-- (a) Quién espera a quién (vista en vivo durante el interbloqueo)
-- ---------------------------------------------------------------------------
SELECT  bloqueada.pid    AS quien_espera,
        bloqueada.query  AS sentencia_trabada,
        bloqueante.pid   AS quien_bloquea,
        bloqueante.query AS sentencia_que_bloquea
FROM    pg_stat_activity bloqueada
JOIN    pg_stat_activity bloqueante
  ON    bloqueante.pid = ANY(pg_blocking_pids(bloqueada.pid))
WHERE   cardinality(pg_blocking_pids(bloqueada.pid)) > 0;

-- ---------------------------------------------------------------------------
-- (b) Configuración para que el MOTOR anote los interbloqueos en el log
-- ---------------------------------------------------------------------------

-- Ver estado actual:
SHOW log_lock_waits;
SHOW deadlock_timeout;

-- Activar (requiere rol superusuario o config en postgresql.conf):
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();   -- no reinicia el servidor

-- Después de provocar el deadlock, el informe completo queda en el log:
--
--   ERROR:  deadlock detected
--   DETAIL: Process 1234 waits for ShareLock on transaction 5678; ...
--           Process 5678 waits for ShareLock on transaction 1234; ...
--           Process 1234 is the deadlock victim.
--
-- Eso es exactamente lo que la captura de la Figura 7.6 debe mostrar.
-- ============================================================================
