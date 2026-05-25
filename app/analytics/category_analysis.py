import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from app.schemas.expense import Expense
from app.database import SessionLocal
import io
import base64



def build_expense_df():
    db = SessionLocal()
    try:
        expense = db.query(Expense).all()
        details = [
            {
                "category": exp.category,
                "amount": int(exp.amount),
                "date": exp.date.strftime("%Y-%m-%d"),
            }
            for exp in expense
        ]
        return pd.DataFrame(details)
    finally:
        db.close()


def get_plot():
    df = build_expense_df()
    if df.empty:
        return ""

    data = df.groupby("category")["amount"].sum().reset_index()
    sns.barplot(x="category", y="amount", data=data, palette="viridis")
    plt.title('Total Amount by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return image
