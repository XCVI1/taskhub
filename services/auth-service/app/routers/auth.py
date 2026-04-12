from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter()
bearer = HTTPBearer()

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).register(data.email, data.password)

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login(data.email, data.password)

@router.get("/me", response_model=UserResponse)
async def me(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    return await AuthService(db).get_current_user(credentials.credentials)

@router.post("/validate")
async def validate(token: str, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).validate_token(token)
