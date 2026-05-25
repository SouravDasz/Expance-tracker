from pydantic import BaseModel, Field
from typing import Literal

class ExpenseForm(BaseModel):
    amount: float = Field(gt=0)

    category: Literal[
        "shopping",
        "travel",
        "grocery",
        "bills",
        "food",
        "entertainment",
        "others"
    ] = "others"
