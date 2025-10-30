from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.config import settings
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting FrantAI backend...")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔗 Ollama: {settings.ollama_host}")

    yield

    # Shutdown
    print("👋 Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="FrantAI API",
    description="AI-powered digital twin chat for Stan Frant",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


# Health endpoint
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment,
    }


# Root
@app.get("/")
async def root():
    return {"message": "FrantAI API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )
