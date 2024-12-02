from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.logger import ElasticsearchLogger

elastic_logger = ElasticsearchLogger()


class CustomErrorHandlingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", "N/A")

        elastic_logger.info(
            {
                "request_id": request_id,
                "method": request.method,
                "url": request.url.__str__(),
                "message": "Request received",
            }
        )

        try:
            # response = await call_next(request)
            # return response
            response: Response = await call_next(request)

            if response.status_code in {200, 201}:
                elastic_logger.info(
                    {
                        "request_id": request_id,
                        "method": request.method,
                        "url": request.url.__str__(),
                        "status_code": response.status_code,
                        "message": "Pdf is uploaded successfully",
                    }
                )

            return response

        except StarletteHTTPException as exc:
            elastic_logger.error(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "url": request.url.__str__(),
                    "exc_status_code": exc.status_code,
                    "message": exc.detail
                }
                # f"HTTPException: {exc.detail} - Status: {exc.status_code}"
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )

        except Exception as exc:
            elastic_logger.error(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "url": request.url.__str__(),
                    "message": f"Unhandled Exception: {str(exc)}"
                }
            )

            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"},
            )
