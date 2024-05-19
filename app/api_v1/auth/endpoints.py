from typing import Annotated

from fastapi import APIRouter, Body, status

from app.api_v1.auth.dependencies import (
    process_registration_request,
    process_login_request,
    process_get_new_token_request
)
from app.api_v1.auth.schemas import (
    UserRegistrationIn,
    UserLoginIn,
    UserLoginOut,
    GetNewTokenIn,
    GetNewTokenOut,
    UserRegistrationOut,
)

auth_routers = APIRouter(prefix="", tags=["Authentication, authorization and registration"])


@auth_routers.post("/registration/", status_code=status.HTTP_201_CREATED)
async def registration(body_data: Annotated[UserRegistrationIn, Body()]) -> UserRegistrationOut:
    return await process_registration_request(body_data.dict())


@auth_routers.post("/login/", status_code=status.HTTP_200_OK)
async def login(body_data: Annotated[UserLoginIn, Body()]) -> UserLoginOut:
    return await process_login_request(body_data.dict())


@auth_routers.post("/get_new_tokens/", status_code=status.HTTP_200_OK)
async def get_new_tokens(body_data: Annotated[GetNewTokenIn, Body()]) -> GetNewTokenOut:
    return await process_get_new_token_request(body_data.dict())
