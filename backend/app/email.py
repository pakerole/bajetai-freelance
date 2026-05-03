import logging
import subprocess
from typing import Optional

logger = logging.getLogger("bajetai")

RECIPIENT = "pakerole@gmail.com"


def send_submission_notification(
    name: str,
    email: str,
    project_type: str,
    description: str,
    company: Optional[str] = None,
    filename: Optional[str] = None,
):
    """Send an email notification about a new project inquiry via sendmail."""
    subject = f"[bajetAI] New Project Inquiry from {name}"
    company_line = f"Company: {company}" if company else "Company: (not provided)"
    file_line = f"Attachment: {filename}" if filename else "Attachment: none"

    body = f"""From: pakerole@gmail.com
Reply-To: {email}
To: {RECIPIENT}
Subject: {subject}
Content-Type: text/plain; charset=UTF-8

New project inquiry received via bajetAI.my
{'=' * 50}

Name:      {name}
Email:     {email}
{company_line}
Project:   {project_type}

Description:
{description}

{file_line}
"""

    try:
        proc = subprocess.run(
            ["/usr/sbin/sendmail", RECIPIENT],
            input=body.encode("utf-8"),
            timeout=30,
            capture_output=True,
        )
        if proc.returncode != 0:
            logger.warning("sendmail returned non-zero (%d): %s", proc.returncode, proc.stderr.decode(errors="replace"))
    except FileNotFoundError:
        logger.warning("sendmail not found at /usr/sbin/sendmail — email not sent")
    except subprocess.TimeoutExpired:
        logger.warning("sendmail timed out")
    except Exception:
        logger.exception("Failed to send submission notification email")
