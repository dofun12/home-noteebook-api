import json
import uuid
from typing import List

from fastapi import APIRouter
from database.db_manager import DBManager
from pydantic import BaseModel, parse_obj_as

router = APIRouter()

db_host = '192.168.15.101'
db_port = '27018'
db_default = 'note'


def toJson(self, json_object, format_json=False):
    if format_json:
        return json.loads(json.dumps(json_object))
    return json_object


def get_connection() -> DBManager:
    return DBManager(MONGODB_HOST=db_host, MONGODB_PORT=db_port)


class Paper(BaseModel):
    id: str
    elementType: str
    content: str


class Note(BaseModel):
    name: str
    type: str
    papers: list[Paper]


@router.get("/")
async def root():
    db = get_connection()
    list_notes = db.list_all('home-notebook', db_default)
    db.close()
    return list_notes


@router.post("/")
async def add(note: Note):
    db = get_connection()
    if note.name is None:
        return toJson('{"response": "Can\'t Save", "success": false}')
    result = db.insert('home-notebook', db_default, note.dict())
    db.close()
    return result


@router.delete("/{name}")
async def delete(name: str):
    db = get_connection()
    find_query = {'name': name}
    result = db.delete_one('home-notebook', db_default, find_query)
    db.close()
    return result


@router.get("/{name}")
async def getByName(name: str):
    db = get_connection()
    find_query = {'name': name}
    result = db.find_one('home-notebook', db_default, find_query)
    db.close()
    return result


def base_model_to_dict_list(list: list[BaseModel]):
    tmp_array = []
    for base in list:
        tmp_array.append(base.__dict__)
    return tmp_array


@router.put("/{name}")
async def update(name: str, note: Note):
    db = get_connection()
    find_query = {'name': name}
    founded = db.find_one('home-notebook', db_default, find_query, tojson=False)
    if not founded:
        return {'message': 'Not found'}

    response = db.update_one('home-notebook', db_default, find_query, {'$set': {
        'papers': base_model_to_dict_list(note.papers),
    }})
    after_update = db.find_one('home-notebook', db_default, find_query)
    db.close()
    return after_update
