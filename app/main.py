from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import inventory, auth
from db import engine
from models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(inventory.router)
app.include_router(auth.router)


# Redirect / requests to Swagger Docs
@app.get("/", tags=["default"])
async def docs():
    return RedirectResponse(url="/docs")
