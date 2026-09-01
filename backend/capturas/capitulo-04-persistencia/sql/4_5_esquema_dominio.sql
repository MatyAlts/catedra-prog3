-- ============================================================================
-- Capítulo 4 · Figura 4.5 — El esquema de un dominio desde un cliente BD
--
-- Consultas para tomar la captura contra PostgreSQL (base del TPI), desde
-- tu cliente (pgAdmin / DBeaver / DataGrip) o psql.
-- ----------------------------------------------------------------------------
-- En psql, el equivalente de "mostrar el esquema" de cada tabla:
--     \d+ pedido
--     \d+ detalle_pedido
--     \d+ pago
--     \d+ historial_estado_pedido
-- ----------------------------------------------------------------------------
-- CÓMO TOMAR LA CAPTURA (pgAdmin):
--   1. Conectá al PostgreSQL del TPI y creá/abrí la base donde vive el dominio
--      de ventas y trazabilidad (pedido, detalle_pedido, pago, historial).
--   2. Pezá estas consultas en el Query Tool (Tools -> Query Tool) y ejecutalás;
--      la grilla que devuelve es la captura.
--   3. Para la vista "de esquema" con cajas y flechas: expandí la base ->
--      Schemas -> public -> Tables, y sobre una tabla usá Sentido derecho ->
--      Properties (solapas Columns, Constraints, Indexes) o el diagrama E-R
--      (Tools -> ERD / Schema Diff) si tu versión de pgAdmin lo ofrece.
-- ----------------------------------------------------------------------------
-- ESTAS TABLAS NO SE CREAN ACÁ. La figura asume el esquema real del TPI.
-- Si querés ver la FORMA del dominio sin conectar a nada, corré
--     4_5_esquema_dominio.py  (SQLite en memoria, solo para entender).
-- ============================================================================

-- 1) Tablas del dominio de ventas / trazabilidad
SELECT table_name
FROM   information_schema.tables
WHERE  table_schema = 'public'
  AND  table_name IN ('pedido', 'detalle_pedido', 'pago',
                      'historial_estado_pedido')
ORDER  BY table_name;

-- 2) Claves foráneas del dominio (el lado "muchos")
SELECT tc.table_name                                  AS tabla_hija,
       kcu.column_name                                AS columna_fk,
       ccu.table_name                                 AS tabla_padre,
       ccu.column_name                                AS columna_referida
FROM   information_schema.table_constraints tc
JOIN   information_schema.key_column_usage kcu
  ON   tc.constraint_name = kcu.constraint_name
JOIN   information_schema.constraint_column_usage ccu
  ON   ccu.constraint_name = tc.constraint_name
WHERE  tc.constraint_type = 'FOREIGN KEY'
  AND  tc.table_name IN ('pedido', 'detalle_pedido', 'pago',
                         'historial_estado_pedido')
ORDER  BY tc.table_name, kcu.column_name;

-- 3) Restricciones CHECK / PK / UNIQUE del dominio (los garantes de Fig. 4.4)
SELECT table_name, constraint_name, constraint_type
FROM   information_schema.table_constraints
WHERE  table_schema = 'public'
  AND  table_name IN ('pedido', 'detalle_pedido', 'pago',
                      'historial_estado_pedido')
  AND  constraint_type IN ('CHECK', 'PRIMARY KEY', 'UNIQUE')
ORDER  BY table_name, constraint_type;

-- 4) Índices (los únicos / de unicidad garante)
SELECT tablename, indexname, indexdef
FROM   pg_indexes
WHERE  schemaname = 'public'
  AND  tablename IN ('pedido', 'detalle_pedido', 'pago',
                     'historial_estado_pedido')
ORDER  BY tablename;

-- ============================================================================
-- Verificación que acompaña a la figura (Cap. 4, §4.12): contar las consultas
-- de un endpoint de listado. Si son 2 o 3, la precarga está bien; si son 21,
-- falta. Eso NO se ve con un cliente de BD sino con el registro de sentencias
-- (ver script del Capítulo 6, figura 6.6).
-- ============================================================================
