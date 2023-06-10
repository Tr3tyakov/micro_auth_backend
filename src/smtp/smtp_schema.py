from pydantic import BaseModel


class CreateSMTP(BaseModel):
    email_address: str
    smtp_address: str
    smtp_port: str
    email_password: str
    email_login: str
