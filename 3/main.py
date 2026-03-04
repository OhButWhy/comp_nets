from fastapi import FastAPI
from parser import let_par
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    author = Column(String, nullable=False)
    tags = Column(String, nullable=True)
    author_link = Column(String, nullable=True)


# Создаём таблицы (если их нет)
Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Привет! Сервер работает."}


@app.get("/parse")
def parse_url(url: str):
    try:
        quotes = let_par(url)
        with SessionLocal() as db:
            for q in quotes:
                query = db.query(Quote).filter(Quote.text == q["text"])
                exists = query.first()
                if not exists:
                    db.add(
                        Quote(
                            text=q["text"],
                            author=q["author"],
                            tags=q["tags"],
                            author_link=q["author_link"]
                        )
                    )
            db.commit()
        return {"quotes": quotes, "saved": True}
    except Exception as e:
        return {"error": str(e)}


# Получить все цитаты из базы

@app.get("/quotes")
def get_quotes():
    with SessionLocal() as db:
        quotes = db.query(Quote).all()
        result = [
            {
                "id": q.id,
                "text": q.text,
                "author": q.author,
                "tags": q.tags,
                "author_link": q.author_link
            }
            for q in quotes
        ]
    return {"quotes": result}
