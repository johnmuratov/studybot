from aiogram.fsm.state import StatesGroup, State


class AddTaskStates(StatesGroup):
    title = State()
    deadline = State()
    confirm = State()
