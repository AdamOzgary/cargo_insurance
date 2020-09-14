from pydantic import BaseModel
from secret import db_name, db_user, db_host, db_pass, db_port
import psycopg2
import json
import datetime

conn = psycopg2.connect(
    dbname = db_name,
    user = db_user,
    password = db_pass,
    host = db_host,
    port = db_port
)

cur = conn.cursor()

def get_rate(cargo_type, date):
    '''this func return current rate from rates.json'''
    with open('rates.json', encoding='utf-8') as f:
        rates = json.load(f)

    try:
        rates = rates[str(date)]
    except KeyError:
        raise RateListError('not have date')

    for r in rates:
        try:
            if r["cargo_type"] == cargo_type:
                rate = r["rate"]
                break
        except KeyError:
            continue
    else: 
        raise RateListError('have not a cargo type')

    return float(rate)

def calculate_cost(cost, date, cargo_type):
    return round(cost * get_rate(cargo_type, date), 2)

class RateListError(Exception): pass

class Cargo(BaseModel):
    name: str 
    declared_cost: float 
    cargo_type: str 
    date: str

class Answer(BaseModel):
    cargo_id: int
    cargo_name: str 
    cargo_type: str
    date: datetime.date
    declared_cost: float 
    insurance_cost: float

class dbms():
    @staticmethod
    def __from_db(t: tuple):
        d = {
            'cargo_id': t[0],
            'cargo_name': t[1],
            'date': t[3], 
            'cargo_type': t[2], 
            'declared_cost': t[4],
            'insurance_cost': t[5]
        }
        return d

    @staticmethod
    def save(obj: Cargo):
        sql_ins = '''INSERT INTO history VALUES(default, %s, %s, %s, %s, %s)'''
        sql_get = '''SELECT * FROM history WHERE cargoId = (SELECT MAX(cargoId) FROM history)'''

        cost = calculate_cost(obj.declared_cost, obj.date, obj.cargo_type)

        values = (obj.name, obj.cargo_type, obj.date, obj.declared_cost, cost)

        cur.execute(sql_ins, values)
        cur.execute(sql_get)
        from_db = cur.fetchone()
        
        return Answer(**dbms.__from_db(from_db))

    @staticmethod
    def get_item(cargo_id: int):
        sql = '''SELECT * FROM history WHERE cargoId = %s '''
        cur.execute(sql, (cargo_id,))
        from_db = cur.fetchone()

        return Answer(**dbms.__from_db(from_db))

    @staticmethod
    def get_all_items():
        sql = '''SELECT cargoId FROM history'''
        cur.execute(sql)
        cargo_id_tuple = cur.fetchall()
        
        cargoes = []
        for cargo_id in cargo_id_tuple:
            cargoes.append(dbms.get_item(cargo_id))

        return cargoes
            

