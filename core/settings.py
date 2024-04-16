from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    bot_token: str
    database: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(bots=Bots(bot_token=env.str("TOKEN"), database=env.str("DATABASE")))


settings = get_settings(".env")
print(settings)
