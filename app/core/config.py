from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_USER: str
    PG_PASSWORD: str

    class Config:
        env_file = ".env"
# objeto settings da classe Settings
settings = Settings() 

if __name__ == "__main__":
    from pprint import pprint
    pprint(settings.dict())
    print(settings.PG_HOST)

    # from dotenv import load_dotenv
    # load_dotenv()