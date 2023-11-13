import os
from loader import dp, db, bot
from aiogram import types
from data.api import get_library_category, get_books
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import get_book_category_btn, login_menu
import requests
import io
import tempfile

@dp.message_handler(text = "📚 Elektron kutubxona")
async def bot_start(message: types.Message, state=FSMContext):
    books_category = get_library_category()
    if books_category:
        await message.answer("Kutubxona bo'limi. Kerakli bo'limni tanlang.", reply_markup=get_book_category_btn(books_category))
        await state.set_state("book_category")
    else:
        await message.answer("Bo'lim mavjud emas")
    
    
@dp.message_handler(text = "🔙 Ortga", state="book_category") 
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer("Bo'limni tanlang", reply_markup=login_menu())
    await state.finish()




@dp.message_handler(state="book_category")
async def input_password(message: types.Message, state: FSMContext):
    category = get_library_category()
    if category:
        for i in category:
            if i['name'] == message.text:
                book_subcategory = get_library_category(pk=i['id'])
                if book_subcategory:
                    await message.answer("Bo'limni tanlang 2", reply_markup=get_book_category_btn(book_subcategory))
                    await state.update_data({
                        "pk":i['id']})
                    await state.set_state("book_subcategory")
                else:
                    await message.answer("Bo'lim mavjud emas")
                    await state.set_state("book_category")
                break
    else:
        await message.answer("Bo'lim mavjud emas")

        await state.set_state("book_category")
        
@dp.message_handler(text = "🔙 Ortga", state="book_subcategory")
async def bot_start(message: types.Message, state=FSMContext):
    books_category = get_library_category()
    await message.answer("Bo'limni tanlang", reply_markup=get_book_category_btn(books_category))
    await state.set_state("book_category")
    
    
@dp.message_handler(state="book_subcategory")
async def input_password(message: types.Message, state: FSMContext):
    # subcategorys = get_library_category(pk=state['pk'])
    data = await state.get_data()
    pk = data['pk']
    books_category = get_library_category(pk=pk)
    for i in books_category:
        if i['name'] == message.text:
            books = get_books(i['id'])
            if books:
                for i in books:
                    title = i['title']
                    desc = title+ "\n\n"
                    if i['description']:
                        desc += i['description']
                    # if i['photo']:
                    #     await message.answer_photo(types.InputFile.from_url(i['photo']), caption=title)
                    response = requests.get(i['file'])
                    if response.status_code == 200:
                        await message.answer_document(types.InputFile.from_url(i['file']), caption=desc)
                        # await message.answer(f"📚  [{i['title']}]({i['file']}) ", parse_mode=types.ParseMode.MARKDOWN)
                    else:
                        # await message.answer( "Failed to fetch the document from the URL.")
                        pass
                    
            else:
                await message.answer("Bo'limda kitoblar mavjud emas")
                await state.set_state("book_subcategory")
            break
        