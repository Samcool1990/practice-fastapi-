from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas


####SECRET_KEY
###Algorithm
###Expiration 
###
SECRET_KEY = "19d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"##(Arbitrary string from documentation)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = str(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"expire": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)

        id = str(payload.get("users_id"))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError: 
        raise credentials_exception

def get_current_user():
    

