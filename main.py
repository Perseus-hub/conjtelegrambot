import asyncio
import logging
import parser
import voc
import make_keyboard
import os
from aiogram.types import ReplyKeyboardRemove
from string import digits, punctuation
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Text


bot_route = Router()
val_list = None


class Conj(StatesGroup):
    get_mood = State()
    get_tense = State()
    get_word = State()


@bot_route.message(Command("start"))
async def start_message(message: types.message, state: FSMContext):
    await message.answer("Hi! This is VerbsConjugrationBot. Write the word!")
    await state.set_state(Conj.get_word)


@bot_route.message(Command("help"))
async def help_message(message: types.message):
    await message.answer(voc.help_msg)


@bot_route.message(Command("cancel"))
async def cancel_message(message: types.message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


@bot_route.message(Conj.get_mood)
async def get_tense_msg(message: types.message, state: FSMContext):
    if message.text != "Back":
        if message.text in voc.mood:
            global val_list
            val_list = await valid_tense(message.text)
            await state.update_data(get_mood=message.text)
            await message.answer(f"Accepted {message.text}", reply_markup=make_keyboard.keyboard(val_list))
            await state.set_state(Conj.get_tense)
        else:
            await message.answer("Sorry I don't know what do you mean...")
    else:
        await message.answer("We're already back.\nReselect the mood.")

@bot_route.message(Conj.get_tense)
async def get_tense_msg(message: types.message, state: FSMContext):
    if message.text != "Back":
        await state.update_data(get_tense=list(filter(lambda sub: message.text in sub, val_list))[0])
        data = await state.get_data()
        add_text = Text(Bold(data['get_word']), " in ", Bold(data['get_tense']), " is ...")
        await message.answer(**add_text.as_kwargs(), reply_markup=ReplyKeyboardRemove())
        await message.answer(await get_result_message(data))
        await state.clear()
    else:
        await message.answer("Choose the mood.", reply_markup=make_keyboard.mood_keyboard(voc.mood))
        await state.set_state(Conj.get_mood)




@bot_route.message(Conj.get_word, F.text)
async def get_word_msg(message: types.message, state: FSMContext):
    if await check_word(message.text.strip().lower()):
        await state.update_data(get_word=message.text.strip().lower())
        await message.answer("Ok. Choose the mood.", reply_markup=make_keyboard.mood_keyboard(voc.mood))
        await state.set_state(Conj.get_mood)
    else:
        await message.answer("Sorry I don't know what do you mean...")


async def check_word(text):
    for item in digits:
        if text.find(item) != -1:
            return False
    for item in punctuation:
        if text.find(item) != -1:
            return False
    if len(text.split(' ')) > 3:
        return False

    return True


async def valid_tense(text):
    if text == "Indicativo":
        return voc.tense_Ind
    elif text == "Condicional":
        return  voc.tense_Con
    elif text == "Subjuntivo":
        return voc.tense_Sub
    elif text == "Imperativo":
        return voc.tense_Imp
    elif text == "Gerundio":
        return voc.tense_Ger
    else:
        return voc.tense_Par


async def get_result_message(data):
    content = parser.parse(data['get_mood'], data['get_tense'], data['get_word'])
    result_msg = ""
    if not content:
        return "content is empty"
        #return "Nope... Not found.\nCheck your word or mood."
    else:
        for k, v in content.items():
            if k == "":
                result_msg += f" - : {v}\n"
            else:
                result_msg += f"{k} : {v}\n"
        return result_msg


async def main():
    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher()
    dp.include_router(bot_route)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
