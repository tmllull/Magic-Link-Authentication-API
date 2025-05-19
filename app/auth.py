import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def create_magic_link_token(email: str) -> str:
    expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "email": email}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def send_magic_link(email: str, token: str):
    # Create the magic link
    magic_link = f"http://localhost:8000/verify?token={token}"
    mensaje = MIMEMultipart()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = email
    mensaje["Subject"] = "Your Magic Link"
    body = f"""
        Here is your Magic Link: {magic_link}". This link will expire in {ACCESS_TOKEN_EXPIRE_MINUTES} minutes.
        """
    mensaje.attach(MIMEText(body, "plain"))
    try:
        servidor = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.sendmail(SMTP_USER, email, mensaje.as_string())
        servidor.quit()
        print("Magic link email sent successfully")
    except Exception as e:
        print(f"Error sending magic link email: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
