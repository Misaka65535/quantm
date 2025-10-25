from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int  # 0-15
    REDIS_EXPIRE: int  # 过期时间, 60s
