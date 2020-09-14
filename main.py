from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schemas import Cargo, Answer, RateListError, dbms
from typing import List
import json

app = FastAPI()


@app.post('/cost', response_model=Answer)
def cost_of_insurance(cargo_info: Cargo):
    try:
        return dbms.save(cargo_info)
    except RateListError as e:
        return JSONResponse(status_code=422, content=e.args)

@app.get('/cost/{cargo_id}', response_model=Answer)
def get_item_by_id(cargo_id: int):
    try:
        return dbms.get_item(cargo_id)
    except TypeError:
        return JSONResponse(status_code=404, content=['no cargo information'])

@app.get('/cost/list/all', response_model=List[Answer])
def get_all_items():
    items = dbms.get_all_items()
    if len(items) != 0:
        return items
    else: 
        return JSONResponse(status_code=404, content=['empty list'])