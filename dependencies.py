from fastapi import Depends, HTTPException
from models import User
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import decode_access_token
from database import get_db

security = HTTPBearer()
async def get_current_user(
        token = Depends(security),
        db : AsyncSession = Depends(get_db)
):
    try:
        decoding = decode_access_token(token.credentials)

    except ValueError:
        raise HTTPException(
            status_code= 401,
            detail="Invalid or expired token",
        )
    try:
        user_id = int(decoding.get("sub"))


    except (TypeError, ValueError):
        raise HTTPException(
            status_code= 401,
            detail="Invalid or expired token"
        )
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code= 401,
            detail="User not found"
        )

    return user