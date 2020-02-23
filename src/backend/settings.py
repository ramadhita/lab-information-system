from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
DATABASE_URL = 'postgresql+psycopg2://lab_app:lab_app@localhost:5432/labservice'

engine = create_engine(DATABASE_URL, pool_pre_ping=True) #cari option buat nge pool, buat ngebuka enginenya intinya, nanti coba cari lagi
session_factory = sessionmaker(bind=engine) #ini buat nyambungin ke enginenya
sess = scoped_session(session_factory) #buat manggil sessionnya
