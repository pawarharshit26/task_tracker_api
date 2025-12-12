from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Database Configuration
    DATABASE_URL: str
    
    # Application Settings
    ENVIRONMENT: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()