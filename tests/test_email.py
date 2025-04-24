import pytest
from unittest.mock import AsyncMock, patch
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

    
@pytest.mark.asyncio
@patch("app.services.email_service.EmailService.smtp_client.send_email", new_callable=AsyncMock)
async def test_send_markdown_email(mock_send, email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    mock_send.assert_awaited_once()
    # Manual verification in Mailtrap
