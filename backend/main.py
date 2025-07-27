from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import inventory_api

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(inventory_api.router, prefix="/inventory", tags=["Inventory"])

# Health check endpoint
@app.get("/")
def read_root():
    return {"status": "healthy", "message": "VMart API is running"}
