import datetime

from sqlalchemy import Boolean, Column, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./data/magic_links.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Model
class MagicLink(Base):
    __tablename__ = "magic_links"

    token = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)


# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def store_magic_link(db: Session, token: str, email: str, expires_at: datetime):
    magic_link = MagicLink(token=token, email=email, expires_at=expires_at)
    db.add(magic_link)
    db.commit()
    return magic_link


def get_magic_link(db: Session, token: str):
    return db.query(MagicLink).filter(MagicLink.token == token).first()


def mark_token_as_used(db: Session, magic_link: MagicLink):
    magic_link.is_used = True
    db.commit()
