from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register():
    return {"message": "User registered"}

@router.post("/login")
async def login():
    return {"access_token": "fake-jwt-token"}
