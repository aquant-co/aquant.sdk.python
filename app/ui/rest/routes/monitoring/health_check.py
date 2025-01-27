from http import HTTPStatus

from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health")
async def health_check() -> Response:
    return Response(status_code=HTTPStatus.OK)
