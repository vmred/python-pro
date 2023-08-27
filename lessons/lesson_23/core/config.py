from constants import config_path
from pydantic import BaseModel
from yaml import Loader, load


class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str

    def connection_string(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class ApplicationConfig(BaseModel):
    main_database: DatabaseConfig


def _load_config() -> ApplicationConfig:
    with open(config_path, "r") as f:
        config_data = load(f.read(), Loader)
    return ApplicationConfig(**config_data)


config = _load_config()
