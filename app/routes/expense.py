from fastapi import APIRouter, Request, Form,Depends
from fastapi.templating import Jinja2Templates
from datetime import date
from app.models.expense_form_validation import ExpenseForm
from app.database import SessionLocal
from app.schemas.expense import Expense
from fastapi.responses import RedirectResponse
from sqlalchemy import extract
from app.analytics.category_analysis import get_plot
router = APIRouter()

def get_db():
    db=SessionLocal()
    try :
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory=r"C:\Expance tracker\app\templates")





@router.get("/expense")
def show_expense(request: Request, db=Depends(get_db)):

    current_month = date.today().month
    current_year = date.today().year

    expenses = (
        db.query(Expense)
        .filter(
            extract("month", Expense.date) == current_month,
            extract("year", Expense.date) == current_year
        )
        .all()
    )
    image=get_plot()

    total_amount = sum(exp.amount for exp in expenses)
    category=[cat.category for cat in expenses]
    return templates.TemplateResponse(request,name="expense.html",
    context={"total_amount":total_amount,"category":category,"expense":expenses,"chart":image})




@router.get("/expense/add_amount")
def add_amount_page(request: Request, success: int = 0,db=Depends(get_db)):
    current_month = date.today().month
    current_year = date.today().year

    expenses = (
        db.query(Expense)
        .filter(
            extract("month", Expense.date) == current_month,
            extract("year", Expense.date) == current_year
        )
        .all()
    )

    total_amount = sum(exp.amount for exp in expenses)
    return templates.TemplateResponse(request=request,
        name="Add Expense Page.html",
        context={ "success": success,"total_amount":total_amount},
    )


@router.post("/expense/add_amount")
def add_amount(
    request: Request,
    amount: float = Form(...),
    category: str = Form(...),
    description: str = Form(None),
    db=Depends(get_db),
):
    today = date.today()

    # Pydantic validation
    result = ExpenseForm(
        amount=amount,
        category=category
    )

    # SQLAlchemy object
    new_expense = Expense(
        amount=result.amount,
        category=result.category,
        date=today
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return RedirectResponse(url="/expense/add_amount?success=1", status_code=303)

    