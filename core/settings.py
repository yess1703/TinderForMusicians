from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(bots=Bots(bot_token=env.str("TOKEN"), admin_id=env.int("ADMIN_ID")))


settings = get_settings("input.env")
print(settings)
