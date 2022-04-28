from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator
from statistics import mean


class Beer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    name: str
    style: str
    image: int
    flavor: int
    cost: int
    rate: int = 0

    @validator("flavor", "image", "cost")
    def validate_ratings(cls, v, field):
        if v < 1 or v > 10:
            raise RuntimeError(f"{field.name} must be between 1 and 10.")
        return v

    @validator("rate", always=True)
    def calculate_rate(cls, v, values):
        rate = mean([values["flavor"], values["image"], values["cost"]])
        return int(rate)


try:
    brewdog = Beer(name="Brewdog", style="NEIPA", image=7, flavor=8, cost=7)
except RuntimeError:
    print("Generic error")
