from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.schemas import TokenData, UserInDB
from app.auth.service import get_user
from app.core.config import get_settings
from app.core.security import ALGORITHM

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
		subject = payload.get("sub")
		if subject is None:
			raise credentials_exception
		token_data = TokenData(sub=subject)
	except JWTError:
		raise credentials_exception

	user = get_user(token_data.sub)
	if user is None:
		raise credentials_exception
	return user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
	if current_user.disabled:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Inactive user",
		)
	return current_user