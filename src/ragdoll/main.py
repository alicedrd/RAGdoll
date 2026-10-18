from io import BytesIO
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
import logging
import sys

from ragdoll.services.rag import RagEngine
from ragdoll.services.generator import get_generator
from ragdoll.services.retriever import get_retriever
from ragdoll.core.sqldb import get_sessionmaker
from ragdoll.core.config import settings
from ragdoll.core.exceptions import AppException, handle_app_exception, handle_sql_exception
from ragdoll.api.v1.router import main_router

# logger config
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-6s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# app startup & close
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        generator = get_generator(
            settings.llm_provider_type,
            model = settings.llm_provider_model,
            api_key = settings.llm_provider_api_key,
            temperature = settings.llm_temperature
        )
        app.state.retriever = get_retriever(
            settings.retriever_type,
            db_path = settings.retriever_db_path,
            collection_name = settings.retriever_collection_name
        )
        app.state.rag_engine = RagEngine(app.state.retriever, generator)
        app.state.sql_session_maker = get_sessionmaker(
            db_url = settings.sql_db_url
        )
    except Exception as err:
        logger.error(f'Error during app init : {err}', exc_info = True)
        raise RuntimeError(f"App init failed : {err}") from err

    yield

    logger.info("Closing RAG API...")

# app creation
app = FastAPI(
    title = "Alice RAG",
    description = "Modular RAG API",
    version = "0.0.1",
    lifespan = lifespan
)

# exception handlers
app.add_exception_handler(AppException, handle_app_exception)
app.add_exception_handler(SQLAlchemyError, handle_sql_exception)

# binding main router
app.include_router(main_router, prefix="/api/v1")