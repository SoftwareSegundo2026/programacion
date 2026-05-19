from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.auth.schemas import TokenData, UserInDB
from app.auth.service import get_user
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
		subject = payload.get("sub")
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
	logger.info("2. get_current_active_user - tarea=validar usuario activo - recibe token=NO, recibe usuario ya autenticado")
	if current_user.disabled:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Inactive user",
		)
	return current_user