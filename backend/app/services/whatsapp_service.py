from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from loguru import logger
from app.core.config import settings


class WhatsAppService:
    """Service for sending WhatsApp messages via Twilio."""

    def __init__(self):
        self.client = None
        self.from_number = settings.TWILIO_WHATSAPP_NUMBER
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

    def is_configured(self) -> bool:
        """Check if WhatsApp service is properly configured."""
        return self.client is not None

    async def send_message(
        self,
        to_number: str,
        message: str
    ) -> Optional[str]:
        """Send a WhatsApp message.

        Args:
            to_number: Recipient's phone number (with country code, e.g., +1234567890)
            message: Message content

        Returns:
            Message SID if successful, None otherwise
        """
        if not self.is_configured():
            logger.warning("WhatsApp service not configured. Message not sent.")
            return None

        try:
            # Format numbers for WhatsApp
            from_whatsapp = f"whatsapp:{self.from_number}"
            to_whatsapp = f"whatsapp:{to_number}"

            message_obj = self.client.messages.create(
                from_=from_whatsapp,
                body=message,
                to=to_whatsapp
            )

            logger.info(f"WhatsApp message sent. SID: {message_obj.sid}")
            return message_obj.sid

        except TwilioRestException as e:
            logger.error(f"Twilio error: {e.msg}")
            return None
        except Exception as e:
            logger.error(f"WhatsApp send failed: {e}")
            return None

    async def send_hook_message(
        self,
        to_number: str,
        hook_message: str,
        concept_title: str
    ) -> Optional[str]:
        """Send a daily hook message."""
        return await self.send_message(to_number, hook_message)

    async def send_article_link(
        self,
        to_number: str,
        article_url: str,
        concept_title: str
    ) -> Optional[str]:
        """Send the article link after user responds YES."""
        message = f"📚 Here's your deep dive on *{concept_title}*:\n\n{article_url}\n\nHappy learning! 🚀"
        return await self.send_message(to_number, message)

    async def send_weekly_summary(
        self,
        to_number: str,
        streak: int,
        concepts_learned: int,
        next_concept: str
    ) -> Optional[str]:
        """Send weekly progress summary."""
        message = f"""📊 *Your Weekly Progress*

🔥 Current Streak: {streak} days
📖 Concepts Learned: {concepts_learned}

Next up: *{next_concept}*

Keep up the amazing work! 💪"""
        return await self.send_message(to_number, message)


# Singleton instance
whatsapp_service = WhatsAppService()
