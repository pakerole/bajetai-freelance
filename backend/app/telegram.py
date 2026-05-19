import html
import logging

import httpx

logger = logging.getLogger("bajetai")

BOT_TOKEN = ""
CHAT_ID = ""


def init_telegram(bot_token: str, chat_id: str):
    global BOT_TOKEN, CHAT_ID
    BOT_TOKEN = bot_token
    CHAT_ID = chat_id
    if BOT_TOKEN and CHAT_ID:
        logger.info("Telegram notifications enabled (chat_id=%s)", CHAT_ID)
    else:
        logger.info("Telegram notifications disabled — missing token or chat_id")


def send_submission_notification(
    name: str,
    email: str,
    inquiry_type: str,
    description: str,
    company: str | None = None,
    filename: str | None = None,
):
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram notification skipped — not configured")
        return

    # Escape all user input to prevent HTML injection in Telegram
    safe_name = html.escape(name)
    safe_email = html.escape(email)
    safe_company = html.escape(company) if company else ""
    safe_inquiry = html.escape(inquiry_type)
    safe_desc = html.escape(description)
    safe_file = html.escape(filename) if filename else ""

    company_line = f"🏢 {safe_company}" if safe_company else ""
    file_line = f"📎 {safe_file}" if safe_file else ""

    text = (
        f"📩 <b>New Inquiry — bajetAI</b>\n"
        f"{'─' * 30}\n"
        f"👤 <b>Name:</b> {safe_name}\n"
        f"📧 <b>Email:</b> {safe_email}\n"
    )
    if company_line:
        text += f"{company_line}\n"
    text += f"🏷 <b>Type:</b> {safe_inquiry}\n\n"
    text += f"💬 <b>Message:</b>\n{safe_desc}\n"
    if file_line:
        text += f"\n{file_line}\n"

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
            )
            if resp.status_code != 200:
                logger.warning("Telegram API error %d: %s", resp.status_code, resp.text)
            else:
                logger.info("Telegram notification sent for inquiry from %s", name)
    except Exception:
        logger.exception("Failed to send Telegram notification")
