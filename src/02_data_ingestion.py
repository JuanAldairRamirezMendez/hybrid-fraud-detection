import polars as pl
from sqlalchemy import create_engine
import os

# ==========================================
# CONFIGURACIÓN DE CONEXIÓN A POSTGRESQL
# ==========================================
# IMPORTANTE: Reemplace 'su_contraseña_segura' con la contraseña real 
# que estableció cuando creó el usuario 'aldair' en PostgreSQL.
DB_PASSWORD = "*^bykp4hR8WsvD" 
DATABASE_URL = f"postgresql+psycopg2://aldair:{DB_PASSWORD}@localhost:5432/fraud_detection_db"
|
# Crear el motor de conexión (Engine) de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Rutas de los archivos crudos (asegúrese de haber descomprimido el ZIP en data/raw/)
TRANS_FILE = "data/raw/train_transaction.csv"
ID_FILE = "data/raw/train_identity.csv"

def ingest_data_to_postgres():
    print("🚀 Iniciando proceso de ingesta de datos a PostgreSQL...")
    
    # 1. Ingestar Tabla de Transacciones
    print(f"\n📂 [1/2] Leyendo {TRANS_FILE} con Polars...")
    if not os.path.exists(TRANS_FILE):
        print(f"❌ Error: No se encuentra el archivo {TRANS_FILE}. Verifique la ruta.")
        return
        
    df_trans = pl.read_csv(TRANS_FILE)
    print(f"✅ Lectura completa. Filas: {len(df_trans)}, Columnas: {len(df_trans.columns)}")
    
    print("⬇️ Insertando datos en la tabla 'transactions' (Esto puede tomar unos minutos)...")
    # if_table_exists="replace" borra la tabla si ya existe y la recrea. 
    # Útil para la fase de desarrollo. En producción usaríamos "append" o "fail".
    df_trans.write_database(
        table_name="transactions", 
        connection=engine, 
        if_table_exists="replace", 
        engine="sqlalchemy"
    )
    print("✅ Tabla 'transactions' creada y poblada exitosamente.")

    # 2. Ingestar Tabla de Identidad
    print(f"\n📂 [2/2] Leyendo {ID_FILE} con Polars...")
    if not os.path.exists(ID_FILE):
        print(f"❌ Error: No se encuentra el archivo {ID_FILE}. Verifique la ruta.")
        return

    df_id = pl.read_csv(ID_FILE)
    print(f"✅ Lectura completa. Filas: {len(df_id)}, Columnas: {len(df_id.columns)}")
    
    print("⬇️ Insertando datos en la tabla 'identity'...")
    df_id.write_database(
        table_name="identity", 
        connection=engine, 
        if_table_exists="replace", 
        engine="sqlalchemy"
    )
    print("✅ Tabla 'identity' creada y poblada exitosamente.")

    print("\n🎉 ¡Ingesta finalizada! Los datos ya están estructurados en PostgreSQL.")

if __name__ == "__main__":
    ingest_data_to_postgres()