from fastapi import APIRouter, Request, Form,Depends
from fastapi.templating import Jinja2Templates
from datetime import date
from app.models.expense_form_validation import ExpenseForm
from app.database import SessionLocal
from app.schemas.expense import Expense
from fastapi.responses import RedirectResponse

router = APIRouter()

def get_db():
    db=SessionLocal()
    try :
        yield db
    finally:
        db.close()

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
    category: str = Form(...),
    db=Depends(get_db)
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

    return {
        "amount": new_expense.amount,
        "category": new_expense.category,
        "date": new_expense.date
    }

    