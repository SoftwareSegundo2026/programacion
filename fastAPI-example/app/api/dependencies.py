from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.users.schemas import TokenData, UserInDB
from app.users.service import get_user
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.security import ALGORITHM

settings = get_settings()
bearer_scheme = HTTPBearer(auto_error=False, scheme_name="bearerAuth")
logger = get_logger(__name__)


async def get_current_user(
    token: str | None = None,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> UserInDB:
    """Autenticación: lee el JWT del encabezado, verifica que sea válido y devuelve el usuario. Si no es válido, responde 401."""
    logger.info("1. get_current_user - tarea=validar JWT de Authorization Bearer - recibe token=%s", "SI" if credentials is not None else "NO")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise credentials_exception
        token = credentials.credentials
        logger.info("1.1 get_current_user - token recibido desde Authorization Bearer")
    else:
        logger.info("1.1 get_current_user - token recibido por parametro directo en test o llamada interna")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
        token_data = TokenData(sub=subject)
    except JWTError:
        raise credentials_exception

    user = await get_user(None, token_data.sub)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Verifica que el usuario no esté deshabilitado. Si lo está, responde 400."""
    logger.info("2. get_current_active_user - tarea=validar usuario activo - recibe token=NO, recibe usuario ya autenticado")
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


def get_current_admin_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    """Verifica que el usuario sea administrador. Si no lo es, responde 403."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> UserInDB | None:
    """Intenta autenticar, pero si no hay token o es inválido devuelve None (sin error)."""
    if credentials is None:
        return None
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            return None
        return await get_user(None, subject)
    except (JWTError, Exception):
        return None
