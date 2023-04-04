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


settings = Settings()
print(settings.database_name)
