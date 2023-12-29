from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def mood_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    key_1 = [KeyboardButton(text=item) for item in items[::2]]
    key_2 = [KeyboardButton(text=item) for item in items[1::2]]
    return ReplyKeyboardMarkup(keyboard=[key_1, key_2], resize_keyboard=True, input_field_placeholder="Press the button!")
def keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    if len(items) == 1:
        key_1 = [KeyboardButton(text=item) for item in items[::2]]
        key_2 = [KeyboardButton(text=item) for item in items[1::2]]
        return ReplyKeyboardMarkup(keyboard=[key_1, key_2, [KeyboardButton(text="Back")]], resize_keyboard=True, input_field_placeholder="Press the button!")
    else:
        mod_list = list()
        for item in items:
            mod_list.append(item.split(' ', maxsplit=1)[1])

        key_11 = [KeyboardButton(text=item) for item in [item for item in mod_list[::2]][::2]]
        key_12 = [KeyboardButton(text=item) for item in [item for item in mod_list[::2]][1::2]]
        key_21 = [KeyboardButton(text=item) for item in [item for item in mod_list[1::2]][::2]]
        key_22 = [KeyboardButton(text=item) for item in [item for item in mod_list[1::2]][1::2]]
        # key_1 = [KeyboardButton(text=item) for item in mod_list[::2]]
        # key_2 = [KeyboardButton(text=item) for item in mod_list[1::2]]
        return ReplyKeyboardMarkup(keyboard=[key_11, key_12, key_21, key_22, [KeyboardButton(text="Back")]], resize_keyboard=True, input_field_placeholder="Press the button!")