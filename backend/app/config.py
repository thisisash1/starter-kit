from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  """환경 변수 관리"""

  # 애플리케이션 설정
  APP_NAME: str = "FastAPI Starter"
  DEBUG: bool = True

  # 데이터베이스 설정
  DB_HOST: str = "localhost"
  DB_PORT: int = 3306
  DB_USER: str = "root"
  DB_PASSWORD: str = ""
  DB_NAME: str = "fastapi_starter"

  @property
  def DATABASE_URL(self) -> str:
    """MySQL async 연결 URL"""
    return (
      f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
      f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    )

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=True
  )


settings = Settings()
