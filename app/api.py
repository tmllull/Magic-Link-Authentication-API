from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import auth
from . import database as db
from .schemas import EmailSchema

router = APIRouter()


@router.post("/request-magic-link")
async def request_magic_link(
    email_data: EmailSchema, db_session: Session = Depends(db.get_db)
):
    """Request a magic link to be sent to the provided email."""
    try:
        # Create token
        token = auth.create_magic_link_token(email_data.email)

        # Store token in database
        expires_at = datetime.now() + timedelta(
            minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        db.store_magic_link(db_session, token, email_data.email, expires_at)

        # Send magic link email
        await auth.send_magic_link(email_data.email, token)

        return {"message": "Magic link sent successfully"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verify")
async def verify_magic_link(token: str, db_session: Session = Depends(db.get_db)):
    """Verify the magic link token and authenticate the user."""
    try:
        # Check if token exists and hasn't been used
        magic_link = db.get_magic_link(db_session, token)
        if not magic_link:
            raise HTTPException(status_code=401, detail="Token not found")

        if magic_link.is_used:
            raise HTTPException(status_code=401, detail="Token has already been used")

        if magic_link.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")

        # Mark token as used
        db.mark_token_as_used(db_session, magic_link)

        # Verify JWT
        payload = auth.verify_token(token)

        return {"message": "Authentication successful", "email": payload["email"]}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
