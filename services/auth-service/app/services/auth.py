from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.core.security import hash_password, verify_password, create_access_token, decode_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, email: str, password: str):
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        hashed = hash_password(password)
        user = await self.repo.create(email=email, hashed_password=hashed)
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    async def login(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    async def get_current_user(self, token: str):
        user_id = decode_token(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def validate_token(self, token: str) -> dict:
        user_id = decode_token(token)
        if not user_id:
            return {"valid": False, "user_id": None}
        return {"valid": True, "user_id": user_id}
