from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    hashed_password: str

    class Config:
        orm_mode = True

class UserInventorySchema(BaseModel):
    user_id: int
    ingredient_id: int
    measurement_unit: str
    quantity: float

    class Config:
        orm_mode = True


