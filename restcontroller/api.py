from fastapi import APIRouter

from restcontroller import root, tarefas_api, notes_api

API_CONTEXT = "/api"

router = APIRouter()
router.include_router(root.router, tags=["root"])
router.include_router(tarefas_api.router, tags=["tarefas"], prefix="/tarefas")
router.include_router(notes_api.router, tags=["notes"], prefix="/notes")
