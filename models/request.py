from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ProductRequest(BaseModel):
    name: str = Field(
        None, title = "Product Name", max_length = 1000
    )
    price: float = Field(..., gt = 0, description = "Price of the product")
    is_available: bool = Field(
        False, description = "Value must be either True or False")
    seller_email: EmailStr = Field(None, title="Seller Email")
    created_by: int = Field(None, title="User Id")

class ProductUpdateRequest(BaseModel):
    product_id: int
    name:str = Field(
        None, title = "Product Name", max_length = 1000
    )
    price: float = Field(..., gt=0, description = "The price must be greater than zero")
    is_available:bool = Field(False, description = "Value must be either True or False")
    seller_email: Optional[EmailStr] = Field(None, title = "Updater Email")
    updated_by:int = Field(None, title = "Updater Id")

class UsersRequest(BaseModel):
    username: str = Field(None, title= "Username", max_length= 100)
    firstName: str = Field(None, title = "User First Name", max_length= 200)
    lastName: str = Field(None, title = "User Last Name", max_length= 200)
    email: EmailStr = Field(None, title = "Users Email")
    password: str = Field(None, title = "Password User", max_length= 50)
    phoneNumber:float = Field(None, title = "Phone Numbers")
    address:str = Field(None, title = "Users Address", max_length= 200)

class UsersUpdateRequest(BaseModel):
    users_id = int
    username: str = Field(None, title = "Username", max_length= 1000)
    firstName: str = Field(None, title = "Updater User First Name", max_length= 200)
    lastName: str = Field(None, title = "Updater User Last Name", max_length= 200)
    email: EmailStr = Field(None, title = "Updater User Email")
    password: str = Field(None, title = "Updater Password User", max_length= 50)
    phoneNumber:float = Field(None, title = "Updater Phone Numbers")
    address:str = Field(None, title = "Updater Users Address", max_length= 200)