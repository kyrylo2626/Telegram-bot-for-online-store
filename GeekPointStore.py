# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as BS
import asyncio
import config
import logging
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

#log_level
logging.basicConfig(level = logging.INFO)

#bot_init
bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

#cart
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cart'))
async def process_callback_katalog_second(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    answer_back_mas = callback_query.data.split("@")

#print_katalog
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('kat1'))
async def process_callback_katalog_second(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    answer_back_mas = callback_query.data.split("@")
    k1 = 0
    if answer_back_mas[1] == "back":
        await katalog(callback_query)
        callback_query.message.message_id = callback_query.message.message_id - 1
        await callback_query.message.delete()
        return True
    else:
        r = requests.get('https://geek-point.com.ua/')
        soup = BS(r.content, 'html.parser')
        list_product = soup.find("ul", {"class": "box-category first-lvl"})
        call_back_info = CallbackData('kat1', 'name_katalog')
        a = 0
        for name in list_product.find_all("li"):
            if a == 1:
                break
            for el in name.find_all("a", {"class": "first-lvl-a"}):
                if el.string == answer_back_mas[2] or el.get('href') == 'https://geek-point.com.ua/' + answer_back_mas[2] + '/':
                    if el.next_sibling.next_sibling == None:
                        await rozprodazh(callback_query, 1, 0, el.get('href'))
                        a = 1
                        break
                    else:
                        katalog_kb = None
                        for elf in name.find_all("a", {"class": "second-lvl-a"}):
                            post = "kat1@" + "th@" + elf.string
                            if katalog_kb == None:
                                katalog_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(elf.string, 
                                    callback_data = call_back_info.new(name_katalog = post)))
                            else:
                                post = "kat1@" + "th@" + elf.string
                                katalog_kb.add(InlineKeyboardButton(elf.string, 
                                    callback_data = call_back_info.new(name_katalog = post)))
                        katalog_kb.add(InlineKeyboardButton("<", callback_data = "kat1@back"))
                        await bot.send_message(text = '???????????? ?????????????????? "' + answer_back_mas[2] + '":', 
                            chat_id = callback_query.from_user.id, reply_markup = katalog_kb)
                        a = 1
                        break
                else:
                    for name_se in name.find_all("li"):
                        if a == 1:
                            break
                        for bl in name_se.find_all("a", {"class": "second-lvl-a"}):
                            if bl.string == answer_back_mas[2] or bl.get('href') == 'https://geek-point.com.ua/' + answer_back_mas[2] + '/':
                                if bl.next_sibling.next_sibling == None:
                                    await rozprodazh(callback_query, 1, 0, bl.get('href'), k1)
                                    a = 1
                                    break
                                else:
                                    katalog_kb = None
                                    for elf in name_se.find_all("a", {"class": "third-lvl-a"}):
                                        k1 = k1 + 1
                                        post = "kat1@" + "th@" + elf.string + "@" + str(k1) 
                                        if katalog_kb == None:
                                            katalog_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(elf.string, 
                                                callback_data = call_back_info.new(name_katalog = post)))
                                        else:
                                            post = "kat1@" + "th@" + elf.string + "@" + str(k1) 
                                            katalog_kb.add(InlineKeyboardButton(elf.string, 
                                                callback_data = call_back_info.new(name_katalog = post)))
                                    ppost = "kat1@" + "se@" + elf.parent.parent.parent.parent.previous_sibling.previous_sibling.string
                                    katalog_kb.add(InlineKeyboardButton("<", callback_data = call_back_info.new(name_katalog = ppost)))
                                    await bot.send_message(text = '???????????? ?????????????????? "' + answer_back_mas[2] + '":', 
                                        chat_id = callback_query.from_user.id, reply_markup = katalog_kb)
                                    a = 1
                                    break
                            else:
                                for tl in name_se.find_all("a", {"class": "third-lvl-a"}):
                                    if a == 1:
                                        break
                                    if tl.string == answer_back_mas[2] or tl.get('href') == 'https://geek-point.com.ua/' + answer_back_mas[2] + '/':
                                        if tl.next_sibling.next_sibling == None:
                                            await rozprodazh(callback_query, 1, 0, tl.get('href'), answer_back_mas[3])
                                            a = 1
                                            break

#print_sal_full
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sal'))
async def process_callback_sal(callback_query: types.CallbackQuery):
    answer_back_mas = callback_query.data.split("@")
    if answer_back_mas[1] == "delete":
        await callback_query.message.delete()
        if len(answer_back_mas) == 2:
            return True
        else:
            callback_query.message.message_id = callback_query.message.message_id - 1
            await callback_query.message.delete()
            return True
    else:
        link = 'https://geek-point.com.ua/' + answer_back_mas[3] + '/'
        k1 = int(answer_back_mas[4])
        if k1 != 0 :
                r = requests.get('https://geek-point.com.ua/')
                soup1 = BS(r.content, 'html.parser')
                soup = soup1.find('ul', {'class': 'box-category first-lvl'})
                for element in soup.find_all("a", {"class": 'second-lvl-a'}):
                    if element.get('href') == link:
                        perg2 = element.next_sibling.next_sibling
                        break
                for elf in perg2.find_all("a", {"class": 'third-lvl-a'}):
                    if k1 == 0:
                        break
                    k1 = k1 - 1
                    link = elf.get('href')
        call_back_info = CallbackData('sal', 'name_and_pic_sal')
        if answer_back_mas[1] == "go":
            await callback_query.message.delete()
            await rozprodazh(callback_query, int(answer_back_mas[2]) + 1, 0, link, answer_back_mas[4])
        elif answer_back_mas[1] == "back":
            await callback_query.message.delete()
            await rozprodazh(callback_query, int(answer_back_mas[2]) - 1, 0, link, answer_back_mas[4])
        elif answer_back_mas[1] == str(1):
            r2 = requests.get(link)
            callback_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('???????????????? ???? ??????????', url = out(r2)[2][int(answer_back_mas[2])]))
            #callback_kb.add(InlineKeyboardButton('???????????? ?? ??????????', callback_data = f"cart@{out(r2)[2][int(answer_back_mas[2])]}"))
            callback_kb.add(InlineKeyboardButton('??????????', callback_data = "sal@delete"))
            await bot.send_photo(chat_id = callback_query.from_user.id, photo = out(r2)[1][int(answer_back_mas[2])], 
                caption = out(r2)[0][int(answer_back_mas[2])], reply_markup = callback_kb)
        else:
            r2 = requests.get(link + '/?page=' + str(answer_back_mas[1]) + '/')
            callback_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('???????????????? ???? ??????????', url = out(r2)[2][int(answer_back_mas[2])]))
            #callback_kb.add(InlineKeyboardButton('???????????? ?? ??????????', callback_data = f"cart@{out(r2)[2][int(answer_back_mas[2])]}"))
            callback_kb.add(InlineKeyboardButton('??????????', callback_data = "sal@delete"))
            await bot.send_photo(chat_id = callback_query.from_user.id, photo = out(r2)[1][int(answer_back_mas[2])], 
                caption = out(r2)[0][int(answer_back_mas[2])], reply_markup = callback_kb)


#text_print_sal
def show_price(link):
    tut = link.replace(" ", "")
    tut = tut.replace("\n", "")
    tut = tut.replace("??????", "")
    tut = tut.replace(".", "")
    return tut

#sal_print
def out(rost):
    name_sal = []
    sal_pic = []
    sal_href = []
    soup_b = BS(rost.content, 'html.parser')
    for soup_div in soup_b.find_all("div", {"class": "product-cell"}):
        hh = soup_div.find("a")
        sal_href.append(hh.get('href'))
        for div in soup_div.find_all("div", {"class": "name"}):
            for img in soup_div.find_all("img"):
                sal_pic.append(img.get('src'))
                for div2 in soup_div.find_all("div", {"class": "price"}):
                    if div2.find_all("span", {"class": "price-new"}):
                        for div3 in div2.find_all("span", {"class": "price-new"}):
                            for el in div.find_all('a'):
                                answer = el.string + ' - ' + show_price(div3.string) + " ??????"
                                name_sal.append(answer)
                    else:
                        for el in div.find_all('a'):
                            answer = el.string + ' - ' + show_price(div2.string) + " ??????"
                            name_sal.append(answer)
    return name_sal, sal_pic, sal_href

#rozprodazh (show product list)
async def rozprodazh(message: types.Message, score = 1, schet = 0, r3 = 'https://geek-point.com.ua/rozprodazh/', k1 = 0):
  r = requests.get(r3)
  soup = BS(r.content, 'html.parser')
  list_product = soup.find("div", {"class": "pagination"})
  num1 = list_product.find("div", {"class": "results"})
  num = num1.string
  call_back_info = CallbackData('sal', 'name_and_pic_sal')
  call_back_info2 = CallbackData('kat1', 'name_and_pic_sal')
  r41 = r3.index("/", 26)
  try:
      r4 = r3.index("/", r41+1)
  except ValueError:
      r4 = r41
  if score == 1:
      r2 = requests.get(r3)
      for i in out(r2)[0]:
          if schet == 0:
              post = "sal@" + str(score) + "@" + str(schet) + "@" + r3[26:r4] + "@" + str(k1)
              sal_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(i, 
                callback_data = call_back_info.new(name_and_pic_sal = post)))
          else:
              post = "sal@" + str(score) + "@" + str(schet) + "@" + r3[26:r4] + "@" + str(k1)
              sal_kb.add(InlineKeyboardButton(i, 
                callback_data = call_back_info.new(name_and_pic_sal = post)))
          schet = schet + 1
      if int(num[-2]) != 1:
          post2 = "sal@" + "go@" + str(score) + "@" + r3[26:r4] + "@" + str(k1)
          sal_kb.add(InlineKeyboardButton(">", callback_data = call_back_info.new(name_and_pic_sal = post2)))
      if r3 == 'https://geek-point.com.ua/rozprodazh/':
          sal_kb.add(InlineKeyboardButton('??????????', callback_data = "sal@delete"))
      else:
          if r4 != r41:
              if k1 != 0:
                  nazad = "kat1@" + "th@" + r3[26:r4]
              else:
                  nazad = "kat1@" + "th@" + r3[26:r41]
          else:
              nazad = "kat1@" + "back"
          sal_kb.add(InlineKeyboardButton('??????????', callback_data = call_back_info2.new(name_and_pic_sal = nazad)))
      await bot.send_message(text = '???? ???????????????????????? ???????????????? ' + str(score) + " ???? " + num[-2] + ":", 
        chat_id = message.from_user.id, reply_markup = sal_kb)
  else:
      r2 = requests.get(r3 + "?page=" + str(score))
      for i in out(r2)[0]:
          if schet == 0:
              post = "sal@" + str(score) + "@" + str(schet) + "@" + r3[26:r4] + "@" + str(k1)
              sal_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(i, 
                callback_data = call_back_info.new(name_and_pic_sal = post)))
          else:
              post = "sal@" + str(score) + "@" + str(schet) + "@" + r3[26:r4] + "@" + str(k1)
              sal_kb.add(InlineKeyboardButton(i, 
                callback_data = call_back_info.new(name_and_pic_sal = post)))
          schet = schet + 1
      if score != int(num[-2]):
          post2 = "sal@" + "go@" + str(score) + "@" + r3[26:r4] + "@" + str(k1)
          post3 = "sal@" + "back@" + str(score) + "@" + r3[26:r4] + "@" + str(k1)
          sal_kb.row(InlineKeyboardButton("<", callback_data = call_back_info.new(name_and_pic_sal = post3)), 
            InlineKeyboardButton(">", callback_data = call_back_info.new(name_and_pic_sal = post2)))
      else:
          post3 = "sal@" + "back@" + str(score) + "@" + r3[26:r4] + "@" + str(k1)
          sal_kb.add(InlineKeyboardButton("<", callback_data = call_back_info.new(name_and_pic_sal = post3)))
      if r3 == 'https://geek-point.com.ua/rozprodazh/':
          sal_kb.add(InlineKeyboardButton('??????????', callback_data = "sal@delete"))
      else:
          if r4 != r41:
              if k1 != 0:
                  nazad = "kat1@" + "th@" + r3[26:r4]
              else:
                  nazad = "kat1@" + "th@" + r3[26:r41]
          else:
              nazad = "kat1@" + "back"
          sal_kb.add(InlineKeyboardButton('??????????', callback_data = call_back_info2.new(name_and_pic_sal = nazad)))
      await bot.send_message(text = '???? ???????????????????????? ???????????????? ' + str(score) + " ???? " + num[-2] + ":", 
        chat_id = message.from_user.id, reply_markup = sal_kb)

#kontakty
async def kontakty(message: types.Message):
    await message.answer("""???? ????????????: ??. ????????, ??????. ????????????????????, 162 (???????? ?? ???????????????????? ??????. ???????????????????? ?? ??????. ??????????????)

???? ?????????????? ???????????? ?? 11:00 ???? 19:00, ?? ?? 12:00 ???? 18:00 ?? ?????????????? ???? ???????????????? ??????

?????? ?????????? ?????? ????????????????: <a href = "tel:0633973438">063-397-34-38</a>
???? ?????????? ?????? ??????????????????????: <a href = "tel:0934323369">093-432-33-69</a>

?????? ?????????????????? ????????????: <a href = "alexei.demchuk@gmail.com">alexei.demchuk@gmail.com</a>""", 
reply_markup=kb_kontakty(), parse_mode=types.ParseMode.HTML)

#start_button_menu
def kb():
    button_hi1 = KeyboardButton('?????????????? ?????????????? ????')
    button_hi2 = KeyboardButton('?????????????????? ????')
    button_hi3 = KeyboardButton('???????????????? ????')

    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi1).row(button_hi2, button_hi3)
    return greet_kb

#kontakty_button
def kb_kontakty():
    button_site = InlineKeyboardButton('?????????????? ???? ????????', url = 'https://geek-point.com.ua/')
    button_tg = InlineKeyboardButton('???????????????? ?? ??????????????????', url = 'https://t.me/380934323369')
    button_instagram = InlineKeyboardButton('Instagram', url = 'https://www.instagram.com/geek_point/')
    button_facebook = InlineKeyboardButton('Facebook', url = 'https://www.facebook.com/geek.point.ua/')
    button_nazad = InlineKeyboardButton('??????????', callback_data = 'sal@delete')

    inline_kb1 = InlineKeyboardMarkup().add(button_site).add(button_tg).row(button_instagram, button_facebook).add(button_nazad)
    return inline_kb1

#katalog_menu
async def katalog(message: types.Message):
    r = requests.get('https://geek-point.com.ua/')
    soup = BS(r.content, 'html.parser')
    list_product = soup.find("ul", {"class": "box-category first-lvl"})
    call_back_info = CallbackData('kat1', 'name_katalog')
    katalog_kb = None
    for el in list_product.find_all("a", {"class": "first-lvl-a"}):
        if el.string == "??????????????????????????????" or el.string == "??????????????????":
            pass
        elif katalog_kb == None:
            post = "kat1@" + "se@" + el.string
            katalog_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(el.string, 
                callback_data = call_back_info.new(name_katalog = post)))
        else:
            post = "kat1@" + "se@" + el.string
            katalog_kb.add(InlineKeyboardButton(el.string, 
                callback_data = call_back_info.new(name_katalog = post)))

    katalog_kb.add(InlineKeyboardButton('??????????', callback_data = 'sal@delete@peace'))
    await bot.send_message(text = '?????????????? ?????????????????? ????????????:', chat_id = message.from_user.id, reply_markup = katalog_kb)

#menu_button
async def menu(message: types.Message):
    if message.text == "?????????????? ?????????????? ????":
        await katalog(message)
    elif message.text == "?????????????????? ????":
        await rozprodazh(message, 1, 0)
    elif message.text == "???????????????? ????":
        await kontakty(message)
    else:
        await message.answer("???????? ??????????, ?????????????? ??????????????????, ???? ?????? ????????????????!", reply_markup=kb())

#bot""
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("???? ?????? ?????????????????", reply_markup=kb())

@dp.message_handler()
async def msg(message: types.Message):
    await menu(message)

#run
if __name__ == "__main__":
  executor.start_polling(dp, skip_updates = True)
