from pydantic import BaseModel, EmailStr, Field

from app.models.role import UserRoles


class UserRegistrationIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, pattern=r".*[0-9].*")
    confirm_password: str = Field(min_length=8, pattern=r".*[0-9].*")
    role_name: UserRoles

    # We can also add here phone_number, name and so on... but I keep it maximum simple 🙂
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "email": "your_email@example.com",
                "password": "y0ur_password",
                "confirm_password": "y0ur_password",
                "role_name": "admin"
            }
        }


class UserRegistrationOut(BaseModel):
    email: EmailStr
    role_name: UserRoles


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    class Config:
        use_enum_values = True

        json_schema_extra = {
            "example": {
                "email": "your_email@example.com",
                "password": "y0ur_password",
            }
        }


class UserLoginOut(BaseModel):
    access_token: str
    refresh_token: str


class GetAccessTokenIn(BaseModel):
    refresh_token: str


class GetAccessTokenOut(BaseModel):
    access_token: str
