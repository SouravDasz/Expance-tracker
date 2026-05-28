from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine,Base
from app.schemas.expense import Expense
from app.routes.expense import router as expense_router
from app.routes.analytics import router as analytics_router
from app.routes.history import router as history
app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(expense_router)
app.include_router(analytics_router)
app.include_router(history)

templates=Jinja2Templates(directory=r"C:\Expance tracker\app\templates")

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(request,name="home.html")