from sqlalchemy.ext.asyncio import AsyncSession
from core.security import hash_password, verify_password, create_access_token
from models.user import User
from schemas.user import UserCreate, UserLogin
from sqlalchemy import select

async def create_user(
        user_info : UserCreate,
        db : AsyncSession
):
    user = await db.execute(select(User).where(User.email == user_info.email))
    result = user.scalar_one_or_none()

    if result is None:
        password = hash_password(user_info.password)

        result = User(
            name=user_info.name,
            email=user_info.email,
            password_hash=password
        )
    else :
        return None

    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def login(
        info : UserLogin,
        db : AsyncSession
):
    user  = await db.execute(select(User).where(User.email == info.email))
    user_result = user.scalar_one_or_none()

    if user_result is None:
        return None

    result = verify_password(info.password, user_result.password_hash)

    if result is False:
        return None

    token = create_access_token(user_result.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
