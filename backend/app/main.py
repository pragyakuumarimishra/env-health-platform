from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Environmental Health Platform API",
    description="Personalized Environmental Health & Air Quality Decision Support Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Env Health Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }