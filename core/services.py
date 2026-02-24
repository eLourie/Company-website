"""
Notification services for contact form submissions.
Handles sending notifications via Telegram and Email.
"""

import logging
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_telegram_notification(contact_message):
    """
    Send notification about new contact message to Telegram bot.

    Args:
        contact_message: ContactMessage model instance

    Returns:
        bool: True if sent successfully, False otherwise
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        logger.warning("Telegram credentials not configured. Skipping notification.")
        return False

    message = (
        f"📨 <b>Новая заявка с сайта {settings.SITE_NAME}</b>\n\n"
        f"👤 <b>Имя:</b> {contact_message.name}\n"
        f"📧 <b>Email:</b> {contact_message.email}\n"
        f"📝 <b>Тема:</b> {contact_message.subject}\n\n"
        f"💬 <b>Сообщение:</b>\n{contact_message.message}\n\n"
        f"🕐 <b>Время:</b> {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        response = requests.post(
            url,
            data={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"Telegram notification sent for message ID: {contact_message.id}")
            return True
        else:
            logger.error(f"Telegram API error: {response.status_code} - {response.text}")
            return False

    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False


def send_email_notification(contact_message):
    """
    Send email notification about new contact message to admin.

    Args:
        contact_message: ContactMessage model instance

    Returns:
        bool: True if sent successfully, False otherwise
    """
    admin_email = settings.ADMIN_EMAIL

    if not admin_email:
        logger.warning("Admin email not configured. Skipping email notification.")
        return False

    subject = f"[{settings.SITE_NAME}] Новая заявка: {contact_message.subject}"

    # Plain text message
    message = (
        f"Новая заявка с сайта {settings.SITE_NAME}\n\n"
        f"Имя: {contact_message.name}\n"
        f"Email: {contact_message.email}\n"
        f"Тема: {contact_message.subject}\n\n"
        f"Сообщение:\n{contact_message.message}\n\n"
        f"Время: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    # HTML message
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #333;">Новая заявка с сайта {settings.SITE_NAME}</h2>
        <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; width: 120px;">Имя:</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{contact_message.name}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">Email:</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">
                    <a href="mailto:{contact_message.email}">{contact_message.email}</a>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">Тема:</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{contact_message.subject}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">Время:</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{contact_message.created_at.strftime('%d.%m.%Y %H:%M')}</td>
            </tr>
        </table>
        <div style="margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 5px;">
            <strong>Сообщение:</strong>
            <p style="white-space: pre-wrap;">{contact_message.message}</p>
        </div>
    </body>
    </html>
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email notification sent for message ID: {contact_message.id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        return False


def send_all_notifications(contact_message):
    """
    Send all configured notifications for a new contact message.

    Args:
        contact_message: ContactMessage model instance

    Returns:
        dict: Results of each notification channel
    """
    results = {
        'telegram': send_telegram_notification(contact_message),
        'email': send_email_notification(contact_message),
    }

    return results
