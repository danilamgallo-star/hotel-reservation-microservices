from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from .schemas import UserCreate, UserResponse, Token
from .config import settings

app = FastAPI(title="Auth Service", version="1.0.0")

# CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@app.get("/")
def read_root():
    return {"service": "Auth Service", "status": "running"}

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Registrar nuevo usuario"""
    # TODO: Verificar si ya existe el usuario
    # TODO: Hashear password y guardar en BD
    return {"id": 1, "email": user.email, "full_name": user.full_name}

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login y devolver token JWT"""
    # TODO: Validar credenciales contra la BD
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/refresh")
async def refresh_token():
    """Renovar el token"""
    return {"message": "Token refreshed"}

@app.post("/api/auth/logout")
async def logout():
    """Cerrar sesión"""
    return {"message": "Successfully logged out"}
