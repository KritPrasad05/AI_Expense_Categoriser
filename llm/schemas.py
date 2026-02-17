from pydantic import BaseModel, Field
from config.categories import CATEGORIES
from typing import Literal, List

class SingleCategorization(BaseModel):
    id: int
    category: Literal[
        "Travel",
        "Meals",
        "Software",
        "Utilities",
        "Marketing",
        "Office Supplies",
        "Entertainment",
        "Healthcare",
        "Other"
    ]
    confidence: float = Field(ge=0.0, le=1.0)


class BatchCategorization(BaseModel):
    results: List[SingleCategorization]

