from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    main_menu_state = State()
    contact_state = State()


class AdminsStates(StatesGroup):
    admin_menu_state = State()
    file_state = State()
    file_name_state = State()

    file_delete_state = State()
    mailing_file_state = State()
    mailing_text_state = State()

