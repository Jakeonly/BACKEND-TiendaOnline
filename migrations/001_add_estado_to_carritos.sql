-- Agregar columna estado a la tabla tbl_carritos
DO $$ BEGIN
  ALTER TABLE tbl_carritos ADD COLUMN estado VARCHAR(20) DEFAULT 'Pendiente' NOT NULL;
EXCEPTION WHEN duplicate_column THEN NULL;
END $$;
