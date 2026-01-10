from fastapi import FastAPI
from models import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables