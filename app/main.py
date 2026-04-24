from fastapi import FastAPI
from app.core.config import settings
from app.api import categories, products

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de Microserviço para E-commerce com FastAPI, PostgreSQL e Redis",
    version="1.0.0",
    debug=settings.DEBUG
)

# Incluir roteadores
app.include_router(categories.router)
app.include_router(products.router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
