from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from app.analytics.category_analysis import build_expense_df

router = APIRouter()

@router.get("/analytics")
def analysis():
    return build_expense_df().to_json(orient="records")