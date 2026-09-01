from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(String(36), primary_key=True)
    nombre_completo = Column(String(80), nullable=False)
metadata = Base.metadata
