from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.domains.user.services import UserService
from app.domains.user.dtos import (
    UserCreateRequest,
    UserCreateResponse,
    UserLoginRequest,
    UserDetailResponse,
)
from app.domains.token.dtos import (
    TokenResponse
)
from app.core.dependencies.providers.get_user_service import get_user_service

router = APIRouter()


@router.post("/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_request: UserCreateRequest, user_service: UserService = Depends(get_user_service)
):
    """
    Register a new user.
    """
    try:
        user = await user_service.register_user(
            username=user_request.username,
            email=user_request.email,
            password=user_request.password,
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_request: UserLoginRequest, user_service: UserService = Depends(get_user_service)
):
    """
    Authenticate a user and return a JWT.
    """
    try:
        token = await user_service.authenticate_user(
            email=login_request.email, password=login_request.password
        )
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )


@router.get("/{user_id}", response_model=UserDetailResponse, status_code=status.HTTP_200_OK)
async def get_user_details(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    """
    Get details of a specific user.
    """
    try:
        # Fetch user and permissions
        user = await user_service.get_user(user_id)
        permissions = await user_service.get_user_permissions(user_id)

        # Ensure the output conforms to `UserDetailResponse`
        user_data = user.model_dump()
        user_data["permissions"] = permissions

        return UserDetailResponse(**user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )