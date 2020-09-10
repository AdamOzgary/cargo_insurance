from pydantic import BaseModel
from datetime import date, datetime

class RateListError(Exception): pass

class Cargo(BaseModel):
    declared_cost: float = None
    cargo_type: str = None
    date: str

class Answer(BaseModel):
    cost: float = None
    error: str = 'no errors'