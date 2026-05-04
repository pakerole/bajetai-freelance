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

    company_line = f"🏢 {company}" if company else ""
    file_line = f"📎 {filename}" if filename else ""

    text = (
        f"📩 <b>New Inquiry — bajetAI</b>\n"
        f"{'─' * 30}\n"
        f"👤 <b>Name:</b> {name}\n"
        f"📧 <b>Email:</b> {email}\n"
    )
    if company_line:
        text += f"{company_line}\n"
    text += f"🏷 <b>Type:</b> {inquiry_type}\n\n"
    text += f"💬 <b>Message:</b>\n{description}\n"
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
