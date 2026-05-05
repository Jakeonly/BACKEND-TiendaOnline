-- Agregar columna estado a la tabla tbl_carritos
ALTER TABLE tbl_carritos ADD COLUMN estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente';
