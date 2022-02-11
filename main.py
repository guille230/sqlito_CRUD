from datetime import datetime
from fastapi import FastAPI, Request
import sqlite3
import json
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DATABASE = '/home/tsi/api_equipo3/grupo3.db'

class UserPost(BaseModel):
    name: str
    password: str
    active: int
    created_at: str


class UserPut(BaseModel):
    name: Optional[str]
    password: Optional[str]
    active: Optional[int]
    created_at: Optional[str]


class ProposalPost(BaseModel):
    title: str
    user_id: int
    created_at: datetime


class ProposalPut(BaseModel):
    title: Optional[str]
    user_id: Optional[int]
    created_at: Optional[datetime]


class CommentPost(BaseModel):
    proposal_id: str
    parent_id: str
    user_id: int
    body: str
    created_at: datetime


class CommentPut(BaseModel):
    proposal_id: Optional[str]
    parent_id: Optional[str]
    user_id: Optional[int]
    body: Optional[str]
    created_at: Optional[datetime]



def sql_json_encode(fields, records, mode=True):
    res = []
    fields_aux = []
    for field in fields:
        fields_aux.append(field[0])
    for record_aux in records:
        dic = {}
        for key, value in zip(fields_aux, record_aux):
            dic[key] = value
        res.append(dic)
    
    return res

# User

@app.get("/user")
async def select_all():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * from User")
    records = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records)

@app.get("/user/{param1}")
async def select_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM User WHERE id=?", (str(param1)))
    records = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records, False)

@app.delete("/user/{param1}")
async def delete_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM User WHERE id=?", (str(param1)))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.post("/user")
async def insert(params: UserPost):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
        
    new_record = (params.id, params.name, params.password, params.active, params.created_at)
    cursor.execute("INSERT INTO User(id, name, password, active, created_at) VALUES(?,?,?,?,?)", (new_record))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.put("/user/{param1}")
async def update(param1: int, params: UserPut):
    variables = []
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    sql = 'UPDATE User SET '
    if params.name:
        sql += 'name = ?,'
        variables.append(params.name)
    if params.password:
        sql += 'password = ?,'
        variables.append(params.password)
    if params.active:
        sql += 'active = ?,'
        variables.append(params.active)
    if params.created_at:
        sql += 'created_at = ?,'
        variables.append(params.created_at)
    
    variables.append(param1)
    sql = sql[:-1] + ' WHERE id = ?'
    cursor.execute(sql, variables)
    records = cursor.fetchall()
    
    cursor.close()
    connection.commit()
    return records

# Proposal

@app.get("/proposal")
async def select_all():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * from Proposal")
    records = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records)

@app.get("/proposal/{param1}")
async def select_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Proposal WHERE id=?", (str(param1)))
    records = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records, False)

@app.delete("/proposal/{param1}")
async def delete_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Proposal WHERE id=?", (str(param1)))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.post("/proposal")
async def insert(params: ProposalPost):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    new_record = (params.id, params.title, params.user_id, params.created_at)
    cursor.execute("INSERT INTO Proposal(id, title, user_id, created_at) VALUES(?,?,?,?)", (new_record))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.put("/proposal/{param1}")
async def update(param1: int, params: ProposalPut):
    variables = []
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if params.title:
        sql += 'name = ?,'
        variables.append(params.title)
    elif params.user_id:
        sql += 'user_id = ?,'
        variables.append(params.user_id)
    elif params.created_at:
        sql += 'created_at = ?,'
        variables.append(params.created_at)
    
    variables.append(param1)
    sql += sql[:-1] + ' WHERE id = ?'
    cursor.execute(sql, variables)
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

# Comment

@app.get("/comment")
async def select_all():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * from Comment")
    records = cursor.fetchall()
    fields = cursor.description

    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records)

@app.get("/comment/{param1}")
async def select_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Comment WHERE id=?", (str(param1)))
    records = cursor.fetchall()
    fields = cursor.description
    cursor.close()
    connection.commit()
    return sql_json_encode(fields, records, False)

@app.delete("/comment/{param1}")
async def delete_with_condition(param1: int):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Comment WHERE id=?", (str(param1)))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.post("/comment")
async def insert(params: CommentPost):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    new_record = (params.id, params.proposal_id, params.parent_id, params.user_id, params.body, params.created_at)
    cursor.execute("INSERT INTO Comment(id, proposal_id, parent_id, user_id, body, created_at) VALUES(?,?,?,?,?,?)", (new_record))
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records

@app.put("/comment/{param1}")
async def update(param1: int, params: CommentPut):
    variables = []
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if params.proposal_id:
        sql += 'name = ?,'
        variables.append(params.proposal_id)
    elif params.parent_id:
        sql += 'active = ?,'
        variables.append(params.parent_id)
    elif user_id:
        sql += 'user_id = ?,'
        variables.append(params.user_id)
    elif params.body:
        sql += 'body = ?,'
        variables.append(params.body)
    elif params.created_at:
        sql += 'created_at = ?,'
        variables.append(params.created_at)
    
    sql += sql[:-1] + ' WHERE id = ?'
    cursor.execute(sql, variables)
    records = cursor.fetchall()

    cursor.close()
    connection.commit()
    return records