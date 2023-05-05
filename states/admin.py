from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    mailing = State()
