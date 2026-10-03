from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class AppException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: dict[str, str] | None = None

    def __init__(self, msg: str, headers: dict[str, str] | None = None):
         super().__init__(msg)
         self.headers = headers

    def to_dict(self):
        return {"message": str(self)}

## FILE VALIDATION & PARSING EXCEPTIONS
# Empty document error
class EmptyDocParsingError(AppException):
    status_code=status.HTTP_400_BAD_REQUEST

    def __init__(self, filename: str):
        super().__init__(f"file empty : {filename}")
        self.filename = filename

    def to_dict(self):
        return {"message": f"{self.filename} is empty."} 

# Unsupported document type error
class UnsupportedDocTypeError(AppException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def __init__(self, filename: str, doc_type: str):
        super().__init__(f"unsupported document type in {filename} : {doc_type}")
        self.filename = filename
        self.doc_type = doc_type

    def to_dict(self):
        return {"message": f"{self.filename} is of an unsupported type ({self.doc_type})."}

# Other error
class OtherFileValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(f"Invalid data")
    
    def to_dict(self):
            return {"message": "Invalid data to ingest."} 

## RETRIEVER EXCEPTIONS
# Document not found in database error
class DocNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, doc_id: str, store: str):
            super().__init__(f"doc id not found in {store} : {doc_id}")
            self.doc_id = doc_id
    
    def to_dict(self):
            return {"message": f"Document {self.doc_id} not found in database."}

## GENERATOR EXCEPTIONS
class PolicyViolatedError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT

class GenerationExhaustedError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT

class ServiceOverloadError(AppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    headers = {"Retry-After": "60"}

class RemoteFailureError(AppException):
    status_code = status.HTTP_502_BAD_GATEWAY

    def __init__(self):
        super().__init__("Remote generator failure")

class RemoteTimeoutError(AppException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT

    def __init__(self):
        super().__init__("Remote timeout exceeded")

class BlacklistViolationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST

class OtherGeneratorError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, msg: str = ""):
        super().__init__(msg)


## Global exception handler
def handle_app_exception(req: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Error due to request {req.url.path} : {exc}", exc_info=True)

    if isinstance(exc, AppException):
        return JSONResponse(
            status_code = exc.status_code,
            content = exc.to_dict()
        )

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {"message": "Internal server error"}
    )

## SQL error handler for uncatched exceptions
# this one is only the one i use for exceptions that must trigger a 500
# if an user GET or DELETE /documents/{id} and this id is missing,
# i try/catch in a service to raise something that triggers a 404 instead
def handle_sql_exception(req: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, SQLAlchemyError)

    logger.error(f"SQL error due to request on {req.url.path} : {exc}", exc_info=True)

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {"message": "Internal server error"}
    )
