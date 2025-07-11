import logging
from email.message import EmailMessage
import aiosmtplib
from typing import Optional
from ..services.notify import send_local_notification

logger = logging.getLogger("mail_service")

DEFAULT_SMTP = {
    "hostname": "smtp.nervura.local",
    "port": 587,
    "username": "",
    "password": "",
    "use_tls": True
}

class SMTPConfig:
    def __init__(
        self,
        hostname: Optional[str],
        port: Optional[int],
        username: Optional[str],
        password: Optional[str],
        use_tls: bool = True,
        enabled: bool = True
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.enabled = enabled

async def send_email(
    to_address: str,
    subject: str,
    html_content: str,
    smtp_config: SMTPConfig,
) -> bool:
    if not smtp_config.enabled:
        logger.warning("SMTP disabled: mail not sent")
        return False

    if not smtp_config.hostname or not smtp_config.port:
        logger.error("SMTP config incomplete: mail not sent")
        await send_local_notification(
            title="SMTP configuration error",
            message="Le serveur SMTP n'est pas configuré correctement. Les mails ne seront pas envoyés."
        )
        return False

    msg = EmailMessage()
    msg["From"] = smtp_config.username or "noreply@nervura.local"
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content("This is a fallback message.")
    msg.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=smtp_config.hostname,
            port=smtp_config.port,
            username=smtp_config.username,
            password=smtp_config.password,
            start_tls=smtp_config.use_tls,
        )
        logger.info(f"Mail sent to {to_address} with subject {subject}")
        return True

    except aiosmtplib.errors.SMTPException as e:
        logger.error(f"SMTP error sending mail: {e}")
        await send_local_notification(
            title="Erreur SMTP lors de l'envoi du mail",
            message=str(e),
        )
        return False


async def check_smtp_config(smtp_config: SMTPConfig) -> None:
    """
    Test la connexion SMTP avec la config donnée.
    Lève HTTPException en cas d'erreur.
    """
    from fastapi import HTTPException

    if not smtp_config.enabled:
        raise HTTPException(status_code=400, detail="SMTP désactivé")

    if not smtp_config.hostname or not smtp_config.port:
        raise HTTPException(status_code=400, detail="Configuration SMTP incomplète")

    try:
        client = aiosmtplib.SMTP(
            hostname=smtp_config.hostname,
            port=smtp_config.port,
            timeout=10,
            start_tls=smtp_config.use_tls,
        )
        await client.connect()
        if smtp_config.username and smtp_config.password:
            await client.login(smtp_config.username, smtp_config.password)
        await client.quit()
    except Exception as e:
        logger.error(f"SMTP config test failed: {e}")
        raise HTTPException(status_code=400, detail=f"Erreur SMTP: {str(e)}")


async def validate_admin_emails(admin_emails: list[str], smtp_config: SMTPConfig) -> bool:
    """
    Vérifie qu'au moins un admin a une adresse mail valide.
    Si aucune adresse, désactive SMTP temporairement et notifie localement.
    """
    valid_emails = [email for email in admin_emails if email]
    if not valid_emails:
        smtp_config.enabled = False
        await send_local_notification(
            title="SMTP désactivé",
            message="Aucune adresse e-mail d'administrateur valide configurée. SMTP désactivé temporairement."
        )
        logger.warning("SMTP désactivé faute d'adresse mail admin")
        return False
    return True
