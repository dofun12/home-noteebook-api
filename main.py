import logging

from starlette.middleware.cors import CORSMiddleware

from restcontroller import api

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S %z')
logger = logging.getLogger('main')


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api.router, prefix='/api')
    return application


app = get_application()



origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
