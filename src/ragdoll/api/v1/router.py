from fastapi import APIRouter
from ragdoll.api.v1.endpoints import admin, chat, documents, search

main_router = APIRouter()

main_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
main_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
main_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
