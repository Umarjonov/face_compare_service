from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os

# .env faylini yuklash
load_dotenv()

# Token sozlamalari
SECRET_KEY = os.getenv("SECRET_KEY")  # .env fayldan olinadi
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default qiymat HS256
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Default qiymat 30 daqiqa

# OAuth2PasswordBearer obyekti
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scheme_name="Bearer")

# Token yaratish funksiyasi
def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Tokenni tekshirish funksiyasi
def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (user_id := payload.get("sub")) is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

router = APIRouter()

@router.post("/token")
async def login_for_access_token(username: str, password: str):
    # Foydalanuvchi ma'lumotlarini tekshirish (misol uchun statik tekshirish)
    if username != "admin" or password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",
        "sub": username,"expire": access_token_expires}