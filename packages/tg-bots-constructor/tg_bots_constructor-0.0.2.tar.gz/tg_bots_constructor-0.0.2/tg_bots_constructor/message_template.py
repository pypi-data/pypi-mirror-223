import json, os
import jinja2

from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .data import Data
from .errors import MessageTemplateError, NotDefinedKeyboardType, NotDefinedTemplate


class MessageTemplate:
    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup|ReplyKeyboardMarkup):
        self.text: str = text
        self.reply_markup: InlineKeyboardMarkup|ReplyKeyboardMarkup = reply_markup

    @classmethod
    def from_json(cls, path: str):
        text, reply_markup = MessageJSONTemplate.load(path)
        return cls(text, reply_markup)
            
    def render(self, data: Data):
        return jinja2.Template(self.text).render(data=data), self.reply_markup


class MessageJSONTemplate:
    @classmethod
    def load(cls, path) -> tuple[str|None, InlineKeyboardMarkup|ReplyKeyboardMarkup|None]:
        template: dict = cls.load_file(path)
        text = cls.load_text(template)
        reply_markup = cls.load_reply_markup(template)
        return text, reply_markup
    
    @staticmethod
    def load_template(path) -> dict:
        if os.path.exists(path):
            try:
                with open(path, encoding='utf-8') as file:
                    return json.load(file)
            except Exception:
                raise MessageTemplateError(path)
            
        raise NotDefinedTemplate(path)
    
    @staticmethod
    def load_text(template: dict) -> str|None:
        text = template.get('text', None)

        if text is not None:
            return ''.join(text)

    @classmethod
    def load_reply_markup(cls, template: dict) -> InlineKeyboardMarkup|ReplyKeyboardMarkup|None:
        keyboard = template.get('keyboard', None)
        
        if keyboard is not None:
            kwargs = {key: value for key, value in keyboard.items() if key not in ['type', 'keys']}
            keys = keyboard['keys']

            match keyboard['type']:
                case 'inline':
                    cls.load_inline_keyboard(keys, kwargs)
                case 'reply':
                    cls.load_reply_keyboard(keys, kwargs)
                case _:
                    raise NotDefinedKeyboardType
                
    @staticmethod
    def load_inline_keyboard(keys, kwargs) -> InlineKeyboardMarkup:
        return InlineKeyboardBuilder(list(map(lambda row: list(map(lambda key: InlineKeyboardButton(**key), row)), keys))).as_markup(**kwargs)
    
    @staticmethod
    def load_reply_keyboard(keys, kwargs) -> ReplyKeyboardMarkup:
        return ReplyKeyboardBuilder(list(map(lambda row: list(map(lambda key: KeyboardButton(**key), row)), keys))).as_markup(**kwargs) 