from fastapi import APIRouter, HTTPException, status

from .schemas import Token, UserLogin
from .service import authenticate_user, create_user_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    credentials: UserLogin,
) -> Token:
    user = await authenticate_user(None, credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_access_token(user)
    return Token(access_token=access_token)