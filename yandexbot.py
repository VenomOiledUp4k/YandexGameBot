import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)

TOKEN = "7662389849:AAFTkGq773-J5PfWP6AytlA4bzo8k9blmEo"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

class UserState(StatesGroup):
    language = State()
    genre = State()

games_info = {
    "Эволюция стихий 2": {
        "description": "Стратегическая игра, где вы развиваете стихии от простых элементов до сложных комбинаций.",
        "genre": "Стратегия",
        "url": "https://yandex.ru/games/app/406195",
        "en_name": "Element Evolution 2",
        "en_description": "A strategic game where you evolve elements from simple to complex combinations.",
        "image_url": "https://avatars.mds.yandex.net/get-games/3006389/2a00000195f6784827ab03fb5c7cad550be0/pjpg128x128"
    },
    "Immortal: Dark Slayer": {
        "description": "Экшен-RPG с темным фэнтези, где вы сражаетесь с монстрами и прокачиваете героя.",
        "genre": "RPG",
        "url": "https://yandex.ru/games/app/367650",
        "en_name": "Immortal: Dark Slayer",
        "en_description": "An action RPG with dark fantasy where you battle monsters and level up your hero.",
        "image_url": "https://avatars.mds.yandex.net/get-games/1881957/2a00000195f1cf0acd029771a6ac744d56c1/pjpg128x128"
    },
    "Твой обби": {
        "description": "Головоломка с интересными уровнями, где нужно преодолевать препятствия.",
        "genre": "Головоломка",
        "url": "https://yandex.ru/games/app/414319",
        "en_name": "Your Obby",
        "en_description": "A puzzle game with interesting levels where you need to overcome obstacles.",
        "image_url": "https://avatars.mds.yandex.net/get-games/12797757/2a000001952ed82409f705ff863d040af8a4/pjpg128x128"
    },
    "Маджонг Дзен сад": {
        "description": "Расслабляющая игра в маджонг с красивой графикой.",
        "genre": "Головоломка",
        "url": "https://yandex.ru/games/app/302697",
        "en_name": "Mahjong Zen Garden",
        "en_description": "A relaxing mahjong game with beautiful graphics.",
        "image_url": "https://avatars.mds.yandex.net/get-games/1881371/2a000001900797c3f490899faa6a9d797f17/pjpg128x128"
    },
    "Домино дуэль": {
        "description": "Классическая настольная игра в домино с режимом дуэли.",
        "genre": "Настольная игра",
        "url": "https://yandex.ru/games/app/199930",
        "en_name": "Domino Duel",
        "en_description": "A classic domino board game with a duel mode.",
        "image_url": "https://avatars.mds.yandex.net/get-games/6238841/2a0000018ea92483ba8d24adb8b1f9cfbc49/pjpg128x128"
    },
    "Live or die Survival": {
        "description": "Выживание в постапокалиптическом мире, где важно принимать правильные решения.",
        "genre": "Выживание",
        "url": "https://yandex.ru/games/app/257333",
        "en_name": "Live or Die Survival",
        "en_description": "Survival in a post-apocalyptic world where making the right decisions is crucial.",
        "image_url": "https://avatars.mds.yandex.net/get-games/11374519/2a0000018c91ddc9e5f9a1bb30429942b5a7/pjpg128x128"
    },
    "Встань на нужный цвет, Робби!": {
        "description": "Аркадная игра с простыми правилами: встаньте на нужный цвет, чтобы победить.",
        "genre": "Аркада",
        "url": "https://yandex.ru/games/app/269613",
        "en_name": "Stand on the Right Color, Robby!",
        "en_description": "An arcade game with simple rules: stand on the right color to win.",
        "image_url": "https://avatars.mds.yandex.net/get-games/11374519/2a0000018bae4e1d9e7ca9ad39112c83640e/pjpg128x128"
    }
}

LANGUAGES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "kk": "🇰🇿 Қазақша"
}

GENRES_TRANSLATIONS = {
    "ru": ["Стратегия", "RPG", "Головоломка", "Настольная игра", "Выживание", "Аркада"],
    "en": ["Strategy", "RPG", "Puzzle", "Board Game", "Survival", "Arcade"],
    "kk": ["Стратегия", "RPG", "Головоломка", "Үстел ойыны", "Тіршілік", "Аркада"]
}

TRANSLATIONS = {
    "ru": {
        "choose_genre": "Выберите жанр:",
        "no_games": "Игры данного жанра не найдены."
    },
    "en": {
        "choose_genre": "Choose genre:",
        "no_games": "No games found in this genre."
    },
    "kk": {
        "choose_genre": "Жанрды таңдаңыз:",
        "no_games": "Бұл жанрда ойындар жоқ."
    }
}

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=LANGUAGES[code])] for code in LANGUAGES],
    resize_keyboard=True
)

def create_genre_keyboard(lang):
    genres = GENRES_TRANSLATIONS.get(lang, GENRES_TRANSLATIONS["ru"])
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=genre)] for genre in genres],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Выберите язык:", reply_markup=language_keyboard)
    await state.set_state(UserState.language)

@dp.message(F.text.in_(LANGUAGES.values()), UserState.language)
async def set_language(message: types.Message, state: FSMContext):
    lang_code = next(code for code, name in LANGUAGES.items() if name == message.text)
    await state.update_data(language=lang_code)
    await message.answer(
        TRANSLATIONS[lang_code]["choose_genre"],
        reply_markup=create_genre_keyboard(lang_code)
    )
    await state.set_state(UserState.genre)

@dp.message(UserState.genre)
async def set_genre(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "ru")
    
    genre_map = {translated: original for original, translated in zip(GENRES_TRANSLATIONS["ru"], GENRES_TRANSLATIONS[lang])}
    selected_genre = genre_map.get(message.text)
    
    if not selected_genre:
        await message.answer(TRANSLATIONS[lang]["no_games"])
        return
    
    filtered_games = {name: info for name, info in games_info.items() if info["genre"] == selected_genre}
    
    if not filtered_games:
        await message.answer(TRANSLATIONS[lang]["no_games"])
        return
    
    buttons = [
        [InlineKeyboardButton(text=info["en_name"] if lang == "en" else name, callback_data=name)]
        for name, info in filtered_games.items()
    ]
    await message.answer(
        TRANSLATIONS[lang]["choose_genre"],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@dp.callback_query()
async def show_game_info(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("language", "ru")
    game = games_info.get(callback.data)
    
    if not game:
        await callback.answer(TRANSLATIONS[lang]["no_games"])
        return
    
    genre_map = {original: translated for original, translated in zip(GENRES_TRANSLATIONS["ru"], GENRES_TRANSLATIONS[lang])}
    translated_genre = genre_map.get(game["genre"], game["genre"])
    
    text = (
        f"<b>{game['en_name'] if lang == 'en' else callback.data}</b>\n"
        f"Жанр: {translated_genre}\n\n"
        f"{game['en_description'] if lang == 'en' else game['description']}\n\n"
        f"Ссылка: {game['url']}"
    )
    
    await callback.message.answer_photo(photo=game["image_url"], caption=text)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())