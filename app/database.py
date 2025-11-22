import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Leemos la configuración del entorno (GitHub Actions o Local)
# Valores por defecto: XAMPP local (root, sin password, localhost, 3306)
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3307")
db_name = os.getenv("DB_NAME", "parcial_db")

# Construimos la URL de conexión para MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Creamos el motor de la base de datos con opciones robustas
# pool_pre_ping=True: Verifica que la conexión esté viva antes de usarla (evita errores de "Lost connection")
# pool_recycle=3600: Recicla conexiones cada hora para evitar timeouts del servidor
# connect_timeout=10: Espera máximo 10 segundos para conectar
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True, 
    pool_recycle=3600,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()