from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

# load .env
load_dotenv()

from core.api.v1.api import router
from core.models.main import create_tables, fill_tables


# create tables
create_tables()

# fill tables
fill_tables()

# FastAPI app
app = FastAPI(
    title="CashSpy API",
    redoc_url=None,
    description="The API documentation of CashSpy server for monitoring of cashback deals from banks.",
)

# allowed origins
origins = [
    "*",
]

# register origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register router
app.include_router(router, prefix="/api")
