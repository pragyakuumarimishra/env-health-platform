from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Environmental Health Platform API",
    description="Personalized Environmental Health & Air Quality Decision Support Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Environmental Health Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "ok"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}