from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SMTPConfig(BaseModel):
    enabled: bool = Field(default=False, description="Activer ou désactiver SMTP")
    hostname: Optional[str] = Field(default=None, description="Adresse du serveur SMTP")
    port: Optional[int] = Field(default=None, description="Port SMTP")
    username: Optional[str] = Field(default=None, description="Nom d'utilisateur SMTP")
    password: Optional[str] = Field(default=None, description="Mot de passe SMTP")
    use_tls: bool = Field(default=True, description="Utiliser TLS pour SMTP")
    from_email: Optional[EmailStr] = Field(default=None, description="Adresse email d'envoi")

class MailSettings(BaseModel):
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True

class MailTest(BaseModel):
    email: EmailStr