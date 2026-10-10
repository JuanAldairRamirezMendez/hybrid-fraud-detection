import pandas as pd
from sqlalchemy import create_engine
import os

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN
# ==========================================
# IMPORTANTE: Reemplace con su contraseña real de PostgreSQL
DB_PASSWORD = "*^bykp4hR8WsvD"
DATABASE_URL = f"postgresql+psycopg2://aldair:{DB_PASSWORD}@localhost:5432/fraud_detection_db"

engine = create_engine(DATABASE_URL)

TRANS_FILE = "data/raw/train_transaction.csv"
ID_FILE = "data/raw/train_identity.csv"

def ingest_data_safe():
    print("🚀 Iniciando ingesta segura por lotes (bajo consumo de RAM)...")
    
    # --- 1. PROCESAR TRANSACCIONES ---
    print(f"\n📂 [1/2] Procesando {TRANS_FILE}...")
    if not os.path.exists(TRANS_FILE):
        print(f"❌ Error: No se encuentra {TRANS_FILE}")
        return

    chunk_size = 50000  # Procesamos de 50,000 en 50,000 filas
    first_chunk = True
    
    # pd.read_csv con chunksize devuelve un iterador, no carga todo en RAM
    for chunk in pd.read_csv(TRANS_FILE, chunksize=chunk_size):
        if first_chunk:
            print("  ➡️ Creando tabla 'transactions' e insertando primer lote...")
            chunk.to_sql("transactions", engine, index=False, if_exists="replace")
            first_chunk = False
        else:
            print(f"  ➡️ Insertando lote de {len(chunk)} filas...")
            chunk.to_sql("transactions", engine, index=False, if_exists="append")
            
    print("✅ Tabla 'transactions' completada exitosamente.")

    # --- 2. PROCESAR IDENTIDAD ---
    print(f"\n📂 [2/2] Procesando {ID_FILE}...")
    if not os.path.exists(ID_FILE):
        print(f"❌ Error: No se encuentra {ID_FILE}")
        return

    first_chunk = True
    for chunk in pd.read_csv(ID_FILE, chunksize=chunk_size):
        if first_chunk:
            print("  ➡️ Creando tabla 'identity' e insertando primer lote...")
            chunk.to_sql("identity", engine, index=False, if_exists="replace")
            first_chunk = False
        else:
            print(f"  ➡️ Insertando lote de {len(chunk)} filas...")
            chunk.to_sql("identity", engine, index=False, if_exists="append")
            
    print("✅ Tabla 'identity' completada exitosamente.")
    print("\n🎉 ¡Ingesta finalizada! Los datos están seguros en PostgreSQL con mínimo uso de RAM.")

if __name__ == "__main__":
    ingest_data_safe()