from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import relationship

from async_session import engine, Base


class Documents(Base):
    __tablename__ = "documents"
    id: int = Column(Integer, primary_key=True)
    path: str = Column(String)
    date: Date = Column(Date, default=datetime.utcnow().date)

    tb1 = relationship("Documents_text", back_populates="tb2")

class Documents_text(Base):
    __tablename__ = "documents_text"
    id: int = Column(Integer, primary_key=True)
    id_doc: int = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'))
    text: str = Column(String)

    tb2 = relationship("Documents", back_populates="tb1")

async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)
#
# async def delete_table():
#     async  with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.drop_all)
