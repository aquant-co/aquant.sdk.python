from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

router = APIRouter()


@router.post("/", response_model=None)
async def telegram_webhook(
    data, service
) -> Response:
    """
    Handles incoming Telegram webhook updates.
    """
    try:
        service.logger.info(f"Validation Passed: {data}")
        return await service.process_webhook_update(data)
    except Exception as e:
        service.logger.error(f"Error processing webhook: {str(e)}")
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
