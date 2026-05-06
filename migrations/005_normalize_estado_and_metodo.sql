-- Migration 005: Normalize estado and metodo values to lowercase and set defaults

-- Set default values to lowercase
ALTER TABLE tbl_carritos ALTER COLUMN estado SET DEFAULT 'pendiente';
ALTER TABLE tbl_ordenes ALTER COLUMN estado SET DEFAULT 'pendiente';
ALTER TABLE tbl_pagos ALTER COLUMN estado SET DEFAULT 'pendiente';

-- Normalize existing data to lowercase
UPDATE tbl_carritos SET estado = lower(estado) WHERE estado IS NOT NULL;
UPDATE tbl_ordenes SET estado = lower(estado) WHERE estado IS NOT NULL;
UPDATE tbl_pagos SET estado = lower(estado) WHERE estado IS NOT NULL;
UPDATE tbl_pagos SET metodo = lower(metodo) WHERE metodo IS NOT NULL;

-- Optional: ensure indexes or constraints remain

