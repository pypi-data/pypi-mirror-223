from fastapi import Request
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from .custom_logging import request_id_contextvar


class AddRequestID(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            fastapi,
    ):
        super().__init__(app)
        self.fastapi = fastapi

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request_id_contextvar.set(request_id)

        response = await call_next(request)
        response.headers["request_id"] = request_id
        return response
