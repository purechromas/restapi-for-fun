from typing import Annotated

from fastapi import APIRouter, Body, status

from app.web.api_v1.auth.dependencies import (
    process_registration_request,
    process_login_request,
    process_access_token_request
)
from app.web.api_v1.auth.schemas import (
    UserRegistrationIn,
    UserLoginIn,
    UserLoginOut,
    GetAccessTokenIn,
    GetAccessTokenOut,
    UserRegistrationOut,
)

auth_routers = APIRouter(prefix="", tags=["Authentication, authorization and registration"])


@auth_routers.post("/registration/", status_code=status.HTTP_201_CREATED)
async def registration(body_data: Annotated[UserRegistrationIn, Body()]) -> UserRegistrationOut:
    return await process_registration_request(body_data.dict())


@auth_routers.post("/login/", status_code=status.HTTP_200_OK)
async def login(body_data: Annotated[UserLoginIn, Body()]) -> UserLoginOut:
    return await process_login_request(body_data.dict())


@auth_routers.post("/get_access_token/", status_code=status.HTTP_200_OK)
async def get_access_token(body_data: Annotated[GetAccessTokenIn, Body()]) -> GetAccessTokenOut:
    return await process_access_token_request(body_data.dict())
