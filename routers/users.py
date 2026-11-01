from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password, create_access_token
from database import get_db
from dependencies import get_current_user
from models import User
from schemas.user import UserResponse, UserCreate, UserLogin
from sqlalchemy import select

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def register_user(
        user_info : UserCreate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == user_info.email))
    user =  result.scalar_one_or_none()
    if user :
        raise HTTPException(status_code=400, detail="User already exists")

    password = hash_password(user_info.password)

    creating_user = User(
        name=user_info.name,
        email=user_info.email,
        password_hash=password
    )

    db.add(creating_user)
    await db.commit()
    await db.refresh(creating_user)
    return creating_user


@router.get("/users/me")
async def check_user(
    user=Depends(get_current_user)
):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


@router.post("/login")
async def login(
        info : UserLogin,
        db: AsyncSession = Depends(get_db)
):
    result  = await db.execute(select(User).where(User.email == info.email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    result = verify_password(info.password, user.password_hash)

    if not result:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
}
