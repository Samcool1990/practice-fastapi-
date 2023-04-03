from pydantic import BaseModel, Field

class Settings(BaseModel):
    database_hostname: str =''
    database_port: str = Field(default='5432')
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings(
    database_hostname= 'localhost',
    database_port= '5432',
    database_password= '321456',
    database_name= 'My FASTAPI DATABSE local',
    database_name= 'postgres', # type: ignore
    secret_key= '19d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7',
    algorithm='HS256',
    access_token_expire_minutes= 60
)
print(settings.database_name)
