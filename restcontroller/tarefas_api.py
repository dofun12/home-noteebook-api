import uuid

from fastapi import APIRouter
from database.db_manager import DBManager
from pydantic import BaseModel

router = APIRouter()

db_host = '192.168.15.101'
db_port = '27018'


def get_connection() -> DBManager:
    return DBManager(MONGODB_HOST=db_host, MONGODB_PORT=db_port)


class Tarefa(BaseModel):
    id: str | None
    name: str
    description: str | None = None
    done: bool


@router.get("/")
async def root():
    db = get_connection()
    list_tarefas = db.list_all('home-notebook', 'tarefas')
    db.close()
    return list_tarefas


@router.post("/")
async def add(tarefa: Tarefa):
    db = get_connection()
    if tarefa.id is None:
        id: str = str(uuid.uuid4())
        tarefa.id = id
    result = db.insert('home-notebook', 'tarefas', tarefa.dict())
    db.close()
    return result


@router.delete("/{id}")
async def delete(id: str):
    db = get_connection()
    find_query = {'id': id}
    result = db.delete_one('home-notebook', 'tarefas', find_query)
    db.close()
    return result


@router.put("/{id}")
async def update(id: str, tarefa: Tarefa):
    db = get_connection()
    find_query = {'id': id}
    founded = db.find_one('home-notebook', 'tarefas', find_query, tojson=False)
    if not founded:
        return {'message': 'Not found'}

    response = db.update_one('home-notebook', 'tarefas', find_query, {'$set': {
        'name': tarefa.name,
        'description': tarefa.description,
        'done': tarefa.done
    }})
    after_update = db.find_one('home-notebook', 'tarefas', find_query)
    db.close()
    return after_update
