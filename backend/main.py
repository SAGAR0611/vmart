from fastapi import FastAPI
from backend.api import inventory_api

app = FastAPI()

app.include_router(inventory_api.router, prefix="/inventory", tags=["Inventory"])

# To run: uvicorn backend.main:app --reload
