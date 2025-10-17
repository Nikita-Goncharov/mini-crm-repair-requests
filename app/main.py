from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import auth, public, admin, worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    yield
    # on shutdown


app = FastAPI(title="Mini-CRM: Repair Requests", lifespan=lifespan)


# Routers
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(admin.router)
app.include_router(worker.router)


@app.get("/")
async def root():
    return {"message": "Mini-CRM Repair Requests API is running"}
