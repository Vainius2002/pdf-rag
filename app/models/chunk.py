from pgvector.sqlalchemy import Vector
from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base

class Chunk(Base):
    __tablename__ = "chunks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    chunk_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))
    
    document: Mapped["Document"] = relationship(back_populates="chunks")
