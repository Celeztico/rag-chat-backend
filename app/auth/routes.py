from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, Token
from app.auth.security import hash_password, verify_password, create_access_token

ALLOW_REGISTRATION = True
MAX_USERS = 5

router = APIRouter(prefix="/auth", tags=["auth"])

# -------------------
# Register
# -------------------

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not ALLOW_REGISTRATION:
        raise HTTPException(403, "Registration is disabled")

    if db.query(User).count() >= MAX_USERS:
        raise HTTPException(403, "User limit reached")

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

# -------------------
# Login (OAuth2)
# -------------------

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

