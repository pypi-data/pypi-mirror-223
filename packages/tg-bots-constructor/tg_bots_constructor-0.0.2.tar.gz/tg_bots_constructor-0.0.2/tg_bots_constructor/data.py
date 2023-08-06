from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, User
from aiogram.fsm.state import State


class Data:
    def __init__(self, 
                 event: Union[Message, CallbackQuery] = None, 
                 state: State = None):
        
        self.message: Message = None
        self.callback: CallbackQuery = None
        self.user: User = None
        self.state: FSMContext = state

        if isinstance(event, Message):
            self.message = event
            self.user = event.from_user
        
        elif isinstance(event, CallbackQuery):
            self.message = event.message
            self.callback = event
            self.user = event.from_user
        