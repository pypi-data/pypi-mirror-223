from dataclasses import dataclass
from aiogram import Bot, Router


@dataclass
class Enviroment:
    bot: Bot = None
    router: Router = None
        