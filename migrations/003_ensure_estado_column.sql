-- Asegurar que la columna estado existe en tbl_carritos
ALTER TABLE IF EXISTS tbl_carritos ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'Pendiente';
