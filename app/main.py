"""Main application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.presentation.api.v1 import api_router
import json
from pathlib import Path
from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Dynamic People Association financial system",
    openapi_url="/dpa/api/v1/openapi.json",
    docs_url="/dpa/docs",
    redoc_url="/dpa/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
# Include API router
app.include_router(api_router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_path = Path("openapi (1).json")
    if openapi_path.exists():
        with open(openapi_path, "r") as f:
            openapi_schema = json.load(f)
            
        # Update paths to include /dpa prefix if not present
        new_paths = {}
        for path, methods in openapi_schema.get("paths", {}).items():
            if not path.startswith("/dpa"):
                new_path = f"/dpa{path}"
            else:
                new_path = path
            new_paths[new_path] = methods
        
        openapi_schema["paths"] = new_paths
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    # Fallback if file doesn't exist
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend API for Dynamic People Association financial system",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



@app.get("/")
def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)
