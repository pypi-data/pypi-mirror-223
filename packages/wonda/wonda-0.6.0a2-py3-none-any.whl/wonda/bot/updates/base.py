from wonda.api import API
from wonda.bot.states import StateRepr


class BaseUpdate:
    ctx_api: API = None
    state_repr: StateRepr | None = None
