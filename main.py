from fastapi import FastAPI
from auth import auth
from db.connect_db import SessionLocal,engine
from db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"message": "OK"}


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(users.router, prefix="/users", tags=["Users"], dependencies=[Depends(verify_token)])
