from fastapi import FastAPI
from app.core.config import settings
from app.api import categories, products
from app.db.session import Base, engine 
from app.models import models # Importar os modelos para criar as tabelas no banco de dados


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de Microserviço para E-commerce com FastAPI, PostgreSQL e Redis",
    version="1.0.0",
    debug=settings.DEBUG
)

# ✅ ESSENCIAL: cria as tabelas no banco ao iniciar
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas/verificadas com sucesso!")

    
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
