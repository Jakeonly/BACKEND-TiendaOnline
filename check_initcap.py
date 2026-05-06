from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import text
from src.database.config import engine

load_dotenv(Path(__file__).resolve().parent / ".env")

with engine.connect() as conn:
    r = conn.execute(text("SELECT DISTINCT metodo FROM tbl_pagos")).fetchall()
    print('Distinct tbl_pagos.metodo ->', [row[0] for row in r])
    r = conn.execute(text("SELECT DISTINCT estado FROM tbl_pagos")).fetchall()
    print('Distinct tbl_pagos.estado ->', [row[0] for row in r])
    r = conn.execute(text("SELECT DISTINCT estado FROM tbl_ordenes")).fetchall()
    print('Distinct tbl_ordenes.estado ->', [row[0] for row in r])
    r = conn.execute(text("SELECT DISTINCT estado FROM tbl_carritos")).fetchall()
    print('Distinct tbl_carritos.estado ->', [row[0] for row in r])
