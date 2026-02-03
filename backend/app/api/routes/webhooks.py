from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.database import get_db
from app.services.scheduler_service import scheduler_service

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming WhatsApp messages from Twilio."""
    try:
        form_data = await request.form()

        # Extract message details
        message_body = form_data.get("Body", "").strip()
        from_number = form_data.get("From", "").replace("whatsapp:", "")
        to_number = form_data.get("To", "").replace("whatsapp:", "")
        message_sid = form_data.get("MessageSid", "")

        logger.info(f"Received WhatsApp message from {from_number}: {message_body}")

        # Process the response
        await scheduler_service.process_user_response(
            db=db,
            phone_number=from_number,
            response=message_body
        )

        # Return empty TwiML response (Twilio expects this)
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
            media_type="application/xml"
        )

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response(
            content='<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
            media_type="application/xml"
        )


@router.get("/whatsapp")
async def whatsapp_webhook_verify(request: Request):
    """Verify webhook endpoint (for Twilio setup)."""
    return {"status": "ok", "message": "WhatsApp webhook endpoint is active"}
