from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
from app.models.expense_form_validation import ExpenseForm
router = APIRouter()

templates = Jinja2Templates(directory=r"C:\Expance tracker\app\templates")


@router.get("/expense")
def show_expense():
    return {"msg": "expense route working"}


@router.get("/expense/add_amount")
def add_amount_page(request: Request):
    return templates.TemplateResponse(request=request,
        name="Add Expense Page.html",
        
    )


@router.post("/expense/add_amount")
def add_amount(
    request: Request,
    amount: float = Form(...),
    category: str = Form(...) ):
    today = date.today()

    # print(today.year)
    result=ExpenseForm(amount=amount,category=category)
    
    output= {
        "amount":result.amount,
        "category":result.category,
        "date":today
    }
    return 

    