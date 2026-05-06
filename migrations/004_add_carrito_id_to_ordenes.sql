-- Migration: add carrito_id column to ordenes
ALTER TABLE tbl_ordenes
ADD COLUMN IF NOT EXISTS carrito_id UUID REFERENCES tbl_carritos(id);

-- Optional: create index for faster lookups by carrito_id
CREATE INDEX IF NOT EXISTS idx_ordenes_carrito_id ON tbl_ordenes (carrito_id);
