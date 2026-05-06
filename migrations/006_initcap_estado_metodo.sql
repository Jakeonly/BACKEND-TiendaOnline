-- 006_initcap_estado_metodo.sql
-- Convierte valores de estado/metodo a Initial Case (Initcap)
BEGIN;

-- Normalizar método y estado en pagos
UPDATE tbl_pagos SET metodo = INITCAP(metodo) WHERE metodo IS NOT NULL;
UPDATE tbl_pagos SET estado = INITCAP(estado) WHERE estado IS NOT NULL;

-- Normalizar estado en órdenes y carritos
UPDATE tbl_ordenes SET estado = INITCAP(estado) WHERE estado IS NOT NULL;
UPDATE tbl_carritos SET estado = INITCAP(estado) WHERE estado IS NOT NULL;

-- Ajustar valores por defecto en las columnas de estado
ALTER TABLE tbl_pagos ALTER COLUMN estado SET DEFAULT 'Pendiente';
ALTER TABLE tbl_ordenes ALTER COLUMN estado SET DEFAULT 'Pendiente';
ALTER TABLE tbl_carritos ALTER COLUMN estado SET DEFAULT 'Pendiente';

COMMIT;
