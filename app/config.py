import os
import pydantic
import yaml
import typing
from pydantic.env_settings import SettingsSourceCallable


def yaml_config_settings_source(
    settings: pydantic.BaseSettings,
) -> typing.Dict[str, typing.Any]:
    encoding = settings.__config__.env_file_encoding
    filename = os.environ.get("CONFIG_FILE", "config.yml")
    if not os.path.exists(filename):
        return {}

    with open(filename, encoding=encoding) as f:
        return yaml.safe_load(f)


class Storage(pydantic.BaseModel):
    dsn: pydantic.RedisDsn = pydantic.Field("redis://localhost:6379/0")


class Telegram(pydantic.BaseModel):
    api_id: int
    api_hash: str


class Bot(pydantic.BaseModel):
    token: str
    destination: int


class Config(pydantic.BaseSettings):
    storage: Storage
    telegram: Telegram
    bot: Bot

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        extra = "ignore"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> typing.Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                file_secret_settings,
                env_settings,
                yaml_config_settings_source,
            )


config = Config()  # type: ignore
