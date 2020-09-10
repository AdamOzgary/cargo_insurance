from fastapi import FastAPI
from schemas import Cargo, Answer, RateListError
import json

app = FastAPI()


def get_rate(obj: Cargo):
    '''this func return current rate from rates.json'''
    with open('rates.json', encoding='utf-8') as f:
        rates = json.load(f)

    try:
        rates = rates[str(obj.date)]
    except KeyError:
        raise RateListError('not have date')

    for r in rates:
        try:
            if r["cargo_type"] == obj.cargo_type:
                rate = r["rate"]
                break
        except KeyError:
            continue
    else: 
        raise RateListError('have not a cargo type')

    return float(rate)


@app.post('/cost', response_model=Answer)
def cost_of_insurance(cargo_info: Cargo):
    answer = Answer()
    if cargo_info.name != None:
        answer.cargo_name = cargo_info.name
        
    try:
        answer.cost = round(cargo_info.declared_cost * get_rate(cargo_info), 2)
    except RateListError as e:
        answer.error = e.args[0]

    return answer