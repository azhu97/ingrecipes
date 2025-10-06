from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    hashed_password: str

    class Config:
        orm_mode = True

