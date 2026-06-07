import time
import uuid

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):

    EXCLUDED_ROUTES = {
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
    }

    def is_excluded(self, path: str) -> bool:
        return any(path.startswith(route) for route in self.EXCLUDED_ROUTES)

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        path = request.url.path

        # Skip auth for public routes
        if self.is_excluded(path):
            response = await call_next(request)
            return response

        # SAFE IP extraction
        client_ip = (
            request.headers.get("x-forwarded-for")
            or (request.client.host if request.client else "unknown")
        )

        # ONLY token header
        token = request.headers.get("X-Service-Token")

        # Missing token
        if not token:
            logger.warning(
                f"auth_failed reason=missing_token request_id={request_id} path={path} ip={client_ip}"
            )

            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "unauthorized",
                    "request_id": request_id,
                    "message": "X-Service-Token header is required",
                },
            )

        # Invalid token
        if token != settings.SERVICE_TOKEN:
            logger.warning(
                f"auth_failed reason=invalid_token request_id={request_id} path={path} ip={client_ip}"
            )

            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "error": "forbidden",
                    "request_id": request_id,
                    "message": "Invalid service token",
                },
            )

        # Proceed
        response = await call_next(request)

        # Add tracing headers
        process_time = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(process_time, 4))

        logger.info(
            f"request_complete request_id={request_id} "
            f"path={path} status={response.status_code} "
            f"duration={process_time:.4f}s"
        )

        return response