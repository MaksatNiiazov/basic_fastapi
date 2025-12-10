__all__ = [
    "api_router",
]

from .v1.router import api_router as v1_router


api_router = v1_router