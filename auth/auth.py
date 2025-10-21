from fastapi import APIRouter, Depends, HTTPException
from auth.jwt import create_access_token
from db.connect_db import SessionLocal
from sqlalchemy.orm import Session
from db.models import User as UserModel
from models.User import Login_Response, User as UserSchema, User_Login, User_Response
from auth.hashPass import verify_password, get_password_hash
from auth.jwt import verify_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post('/signup', response_model=User_Response)
def signup(user: UserSchema, db: Session = Depends(get_db)):
    print(user)
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(user : User_Login ,response_model=Login_Response,db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"access_token": create_access_token(data={"username": existing_user.username})}
    
@router.get("/authenticated")
def authenticated(username: str = Depends(verify_token)):
    return {"message": f"Authenticated as {username}"}