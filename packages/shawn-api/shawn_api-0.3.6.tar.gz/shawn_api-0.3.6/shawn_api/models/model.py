from typing import Optional
from .chat import Chat


class Event(dict):
    chat: Optional[Chat] = Chat()


class Context(dict):
    pass
