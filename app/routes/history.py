from fastapi import APIRouter,Request,Depends
from app.database import SessionLocal
from app.schemas.expense import Expense
from fastapi.templating import Jinja2Templates
from collections import defaultdict
from datetime import datetime
from fastapi.responses import RedirectResponse
router=APIRouter()
templates = Jinja2Templates(directory=r"C:\Expance tracker\app\templates")

@router.get("/history")
def history(request:Request):
    db=SessionLocal()
    records=db.query(Expense).order_by(Expense.date.desc()).all()
    db.close()
    
    # Group records by month
    records_by_month = defaultdict(list)
    for record in records:
        month_key = record.date.strftime("%B %Y")
        records_by_month[month_key].append(record)
    
    total_records = len(records)
    return templates.TemplateResponse(request=request,name="history.html",context={"records_by_month":records_by_month, "total_records": total_records})

@router.post("/delete/{expense_id}")
def delete(request:Request,expense_id:int):
    db=SessionLocal()
    record=db.query(Expense).filter(Expense.id==expense_id).first()
    if record:
        db.delete(record)
        db.commit()
        db.close()
    return RedirectResponse(url="/history",status_code=303)
