from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ArticleCreate
from ..crud import (
    create_article,
    get_articles,
    get_article
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    articles = get_articles(db)

    return templates.TemplateResponse(
    request=request, 
    name="index.html", 
    context={"articles": articles}
)


@router.get("/articles/create", response_class=HTMLResponse)
def create_article_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_article.html",
        
    )


@router.post("/articles/create")
def create_article_submit(
    request:Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    article = ArticleCreate(
        title=title,
        content=content
    )

    create_article(db, article)
    # return render(request.url_for('home'))
    return RedirectResponse(url="/", status_code=303)
    # return {"message": "Article created successfully"}


@router.get("/articles/{article_id}", response_class=HTMLResponse)
def article_detail(
    article_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    article = get_article(db, article_id)

    return templates.TemplateResponse(
        name="article_detail.html",
        request=request,
        context={"article":article}
        
    )