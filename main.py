import os
import time

from decouple import config

from api.routers.api import router as api_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request


debug = config('DEBUG', cast=bool)

if debug:
    app = FastAPI()
    os.environ["OPENAI_API_KEY"] = config('OPENAPI_KEY')
else:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    if debug:
        response.headers["Access-Control-Allow-Origin"] = '*'
    return response

origins = config('ORIGIN', cast=lambda origin: [s.strip() for s in origin.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

