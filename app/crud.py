from sqlalchemy.orm import Session
from .models import Article
from .schemas import ArticleCreate


def create_article(db: Session, article: ArticleCreate):
    db_article = Article(
        title=article.title,
        content=article.content
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


def get_articles(db: Session):
    return db.query(Article).all()


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(
        Article.id == article_id
    ).first()