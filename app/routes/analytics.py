from fastapi import APIRouter, Request, Form,Depends
from fastapi.templating import Jinja2Templates
from app.analytics.category_analysis import df

router=APIRouter()

@router.get("/analytics")
def analysis():
    return df.to_json(orient="records")