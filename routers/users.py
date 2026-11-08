from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import (create_user as create_user_service,
login as login_service )
from database import get_db
from dependencies import get_current_user
from schemas.user import UserResponse, UserCreate, UserLogin

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def register_user(
        user_info : UserCreate,
        db: AsyncSession = Depends(get_db)
):
    result = await create_user_service(user_info, db)

    if result is None :
        raise HTTPException(status_code=400, detail="User already exists")

    return result


@router.get("/users/me",response_model=UserResponse)
async def check_user(
        user=Depends(get_current_user)
):
    return user



@router.post("/login")
async def login(
        info : UserLogin,
        db: AsyncSession = Depends(get_db)
):
    result = await login_service(info, db)

    if result is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return result

