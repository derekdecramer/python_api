from fastapi import Depends, HTTPException, status, APIRouter
from app import models, oauth2, schemas, utils
from app.database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRegister)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())   # unpacked post fields

    user = db.query(models.User).filter(models.User.email == user.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT,
                            detail=f"A user with email: {user.email} already exists.")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("NEW USER")
    print(new_user)
    # print(new_user["id"])

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": new_user.id})

    # return token
    # return {**new_user, "access_token": access_token, "token_type": "bearer"}
    return {"id": new_user.id, "email": new_user.email, "created_at": new_user.created_at, "access_token": access_token, "token_type": "bearer"}

    # return new_user



@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist.")

    return user