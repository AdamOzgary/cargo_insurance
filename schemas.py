from pydantic import BaseModel
from datetime import date, datetime

class RateListError(Exception): pass

class Cargo(BaseModel):
    name: str = None
    declared_cost: float = None
    cargo_type: str = None
    date: str

class Answer(BaseModel):
    cargo_name: str = None
    cost: float = None
    error: str = 'no errors'