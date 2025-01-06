# main.py | kutubxonalar

from telebot import types
from pymovie.config import *
import time
import os
from datetime import  datetime, timedelta
from pymovie.database import *
import random
import traceback
from telebot import types
from telebot.types import Message , InlineKeyboardMarkup, InlineKeyboardButton , ChatPermissions
from telebot.types import Message
import threading


def only_owner(func):
    def wrapper(message):
        chat_id = message.chat.id
        message_id = message.message_id  # Foydalanuvchi yuborgan xabar ID'si

        if message.from_user.id == OWNER_ID:
            return func(message)  # Agar bot egasi bo'lsa, asosiy funksiya bajariladi
        else:
            # Foydalanuvchi ruxsatsiz buyruq bergan xabarni o'chirish
            bot.delete_message(chat_id, message_id)

    return wrapper

def start(msg):
    cid = msg.chat.id
    text = msg.text
    bot.send_chat_action(cid, 'typing')
    url = "https://ibb.co/5sQmCZQ"
    bot.send_photo(cid, url,caption=f"""
😊 <b>Salom  pymovie.uz ga hush kelibsiz</b>

<i>✨ Menga shunchaki Film kodini , nomini yuboring yoki
pastdagi tugmalardan ham foydalanish mumkin...</i>""", reply_markup=main_menu())
    

conn.commit()

# start message
@bot.message_handler(commands=['start'])
@private_chat_only
def welcome(msg):
    cid = msg.chat.id
    text = msg.text
    kl=bot.send_message(cid, f"𝘗𝘙𝘌𝘚𝘚 ➺ /start ....")
    check = cursor.execute(f"SELECT * FROM users WHERE chat_id={cid}").fetchone()
    if check is None:
      cursor.execute(f"INSERT INTO users(chat_id) VALUES({cid})")

    start_param = text.split(' ')[1] if len(text.split(' ')) > 1 else ''

    if start_param == 'dub':
        btn = InlineKeyboardMarkup(row_width=2)
        btn.add(InlineKeyboardButton(text="❕Roziman", callback_data="roziman"))
        bot.delete_message(cid,kl.message_id)
        bot.send_photo(cid, photo="https://telegra.ph/file/e5cab8e289b28061ad5b1.jpg",caption=dub_text,reply_markup=btn)
        return

    elif start_param == 'admin':
        bot.delete_message(cid,kl.message_id)
        bot.send_message(cid, admin_text, reply_markup=adminga())
        return
    elif start_param == 'info':
        bot.delete_message(cid,kl.message_id)
        info(msg)
    elif text=='/start' and len(text)==6:
        bot.delete_message(cid,kl.message_id)
        start(msg)
    elif text.split(" ")[0] and len(text)>5:
      code = text.split(" ")[1]
      if 's' in code  and join(cid):
        code = code.replace("s","")
        all = cursor.execute(f"SELECT * FROM serial WHERE id={code}").fetchone()
        if all:
          name = all[1]
          json = cursor.execute(f"SELECT * FROM movies WHERE serial='{name}'").fetchall()
          c = 0
          key = InlineKeyboardMarkup(row_width=4)
          m = []
          for i in json:
            c+=1
            m.append(InlineKeyboardButton(text=f"{c}",callback_data=f'yukla-{i[0]}'))
          key.add(*m)
          bot.delete_message(cid,kl.message_id)
          sent=bot.send_photo(cid,photo=all[2],caption=f"<b>#{name} \n\n🎬 Qisimlar: {len(json)}</b>",reply_markup=key)
          bot.pin_chat_message(cid, sent.message_id)


def info(msg):
    try:
        # Xabarni foydalanuvchiga yuborish
        bot.copy_message(chat_id=msg.chat.id, from_chat_id=-1002310865207, message_id=5)
    except Exception as e:
        bot.reply_to(msg, f"Xatolik yuz berdi: {e}")



@bot.callback_query_handler(func=lambda call: call.data == "home")
def home_callback(call):
    try:
        bot.answer_callback_query(call.id)

        bot.delete_message(call.message.chat.id, call.message.message_id)

        start(call.message)
    except Exception as e:
        print(f"Xato yuz berdi: {e}")


@bot.message_handler(func=lambda message: message.text == "📣 E'lonlar")
@only_owner
def news_handler(message):
 
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Yangi e'lon qo'shish", callback_data="add_announcement"))
    markup.add(types.InlineKeyboardButton("E'lonlarni o'chirish", callback_data="delete_announcement"))
    bot.send_message(message.chat.id, "E'lonlarni boshqarish bo'limi", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "add_announcement")
def add_announcement(call):
    bot.send_message(call.message.chat.id, "E'lon uchun rasm URL yuboring:")
    bot.register_next_step_handler(call.message, get_photo_url)

def get_photo_url(message):
    photo_url = message.text
    bot.send_message(message.chat.id, "E'lon matnini markdown formatda yuboring:")
    bot.register_next_step_handler(message, get_text, photo_url)

def get_text(message, photo_url):
    text = message.text
    bot.send_message(message.chat.id, "Tugma nomini yuboring:")
    bot.register_next_step_handler(message, get_button_name, photo_url, text)

def get_button_name(message, photo_url, text):
    button_name = message.text
    bot.send_message(message.chat.id, "Tugma URL yuboring:")
    bot.register_next_step_handler(message, save_announcement, photo_url, text, button_name)

def save_announcement(message, photo_url, text, button_name):
    button_url = message.text
    date_added = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO announcements (photo_url, text, button_name, button_url, date_added) VALUES (?, ?, ?, ?, ?)",
                   (photo_url, text, button_name, button_url, date_added))
    
    bot.send_message(message.chat.id, "E'lon saqlandi!")
    
@bot.callback_query_handler(func=lambda call: call.data == "delete_announcement")
def delete_announcement(call):
    cursor.execute("SELECT id, text FROM announcements")
    announcements = cursor.fetchall()

    if not announcements:
        bot.send_message(call.message.chat.id, "Hech qanday e'lon topilmadi.")
        return

    markup = types.InlineKeyboardMarkup()
    for announcement in announcements:
        markup.add(types.InlineKeyboardButton(announcement[1][:30], callback_data=f"dell_{announcement[0]}"))

    bot.edit_message_text("O'chirish uchun e'lonni tanlang:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("dell_"))
def confirm_delete(call):
    announcement_id = int(call.data.split("_")[1])

    cursor.execute("DELETE FROM announcements WHERE id = ?", (announcement_id,))
    conn.commit()

    bot.edit_message_text("E'lon muvaffaqiyatli o'chirildi!", call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "news")
def view_announcements(call):
    cursor.execute("SELECT * FROM announcements")
    announcements = cursor.fetchall()

    if not announcements:
        bot.send_message(call.message.chat.id, "Hozircha e'lonlar mavjud emas.")
        return

    for announcement in announcements:
        cursor.execute("SELECT 1 FROM user_reactions WHERE user_id = ? AND announcement_id = ?", (call.from_user.id, announcement[0]))
        already_viewed = cursor.fetchone()

        if not already_viewed:
            cursor.execute("UPDATE announcements SET views = views + 1 WHERE id = ?", (announcement[0],))
            cursor.execute("INSERT INTO user_reactions (user_id, announcement_id, reaction) VALUES (?, ?, NULL)", (call.from_user.id, announcement[0]))
            

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(announcement[3], url=announcement[4]))
        reactions = [
            types.InlineKeyboardButton(f"❤️ {announcement[7]}", callback_data=f"love_{announcement[0]}"),
            types.InlineKeyboardButton(f"🔥 {announcement[8]}", callback_data=f"fire_{announcement[0]}"),
            types.InlineKeyboardButton(f"⚡️ {announcement[9]}", callback_data=f"lightning_{announcement[0]}"),
            types.InlineKeyboardButton(f"🌼 {announcement[10]}", callback_data=f"flower_{announcement[0]}"),
        ]
        markup.add(*reactions)
        markup.add(types.InlineKeyboardButton(" ⌂ Home", callback_data="home"))

        caption = (
            f"{announcement[2]}\n\n"
            f"📅 : {announcement[5]} | 👁 {announcement[6]}\n"
            
        )

        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=types.InputMediaPhoto(
                media=announcement[1],
                caption=caption,
                parse_mode="Markdown"
            ),
            reply_markup=markup
        )

def generate_announcement_markup(announcement):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(announcement[3], url=announcement[4]))

    # Reaksiyalar tugmalarini bitta qatorda joylashtirish
    reactions = [
        types.InlineKeyboardButton(f"❤️ {announcement[7]}", callback_data=f"love_{announcement[0]}"),
        types.InlineKeyboardButton(f"🔥 {announcement[8]}", callback_data=f"fire_{announcement[0]}"),
        types.InlineKeyboardButton(f"⚡️ {announcement[9]}", callback_data=f"lightning_{announcement[0]}"),
        types.InlineKeyboardButton(f"🌼 {announcement[10]}", callback_data=f"flower_{announcement[0]}"),
    ]
    
    # Qatorga joylashadi
    markup.add(*reactions)

    markup.add(types.InlineKeyboardButton(" ⌂ Home", callback_data="home"))
    return markup



def update_announcement_message(call, announcement):
    caption = (
        f"{announcement[2]}\n\n"
        f"📅 : {announcement[5]} | 👁 {announcement[6]}\n"
    )
    markup = generate_announcement_markup(announcement)
    bot.edit_message_media(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        media=types.InputMediaPhoto(
            media=announcement[1],
            caption=caption,
            parse_mode="Markdown"
        ),
        reply_markup=markup
    )
    


@bot.callback_query_handler(func=lambda call: any(call.data.startswith(r) for r in ["love_", "fire_", "lightning_", "flower_"]))
def reaction_handler(call):
    reaction_type, announcement_id = call.data.split("_")
    announcement_id = int(announcement_id)

    # Foydalanuvchining mavjud reaksiyasini tekshirish
    cursor.execute("SELECT reaction FROM user_reactions WHERE user_id = ? AND announcement_id = ?", (call.from_user.id, announcement_id))
    existing_reaction = cursor.fetchone()

    if existing_reaction and existing_reaction[0] is not None:
        existing_reaction_type = existing_reaction[0]

        if existing_reaction_type == reaction_type:
            bot.answer_callback_query(call.id, "Siz bu reaksiyani allaqachon tanlagansiz!")
            return

        # Eski reaksiyani kamaytirish
        cursor.execute(f"UPDATE announcements SET {existing_reaction_type}s = {existing_reaction_type}s - 1 WHERE id = ?", (announcement_id,))
    else:
        existing_reaction_type = None

    # Yangi reaksiyani oshirish
    cursor.execute(f"UPDATE announcements SET {reaction_type}s = {reaction_type}s + 1 WHERE id = ?", (announcement_id,))
    cursor.execute("REPLACE INTO user_reactions (user_id, announcement_id, reaction) VALUES (?, ?, ?)",
                   (call.from_user.id, announcement_id, reaction_type))

    # Yangilangan e'lonni olish
    cursor.execute("SELECT * FROM announcements WHERE id = ?", (announcement_id,))
    updated_announcement = cursor.fetchone()

    # Yangilangan e'lon xabarini yuborish
    update_announcement_message(call, updated_announcement)

    bot.answer_callback_query(call.id, "Reaksiya qabul qilindi!")




@bot.message_handler(func=lambda message: message.text == "🎴 Kanallarni boshqarish")
@only_owner
def channel_management(message):
    channels = get_channels()
    text = "📋 <b>Mavjud kanallar:</b>\n"
    if channels:
        text += "\n".join([f"• {channel[1]} ({channel[2]})" for channel in channels])
    else:
        text += "❌ Kanallar mavjud emas."
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=generate_admin_panel())

@bot.callback_query_handler(func=lambda call: call.data == "add_channel")
def ask_for_channel_info(call):
    bot.edit_message_text(
        "Kanal nomini yuboring:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    bot.register_next_step_handler(call.message, get_channel_name)

def get_channel_name(message):
    channel_name = message.text
    bot.send_message(message.chat.id, "Kanal URLni yuboring:")
    bot.register_next_step_handler(message, get_channel_url, channel_name)

def get_channel_url(message, channel_name):
    channel_url = message.text
    try:
        add_channel(channel_name, channel_url)
        bot.send_message(
            message.chat.id,
            "✅ Kanal muvaffaqiyatli qo'shildi!",
            reply_markup=generate_admin_panel()
        )
    except ValueError as e:
        bot.send_message(message.chat.id, f"❌ Xato: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "delete_channel")
def ask_for_channel_deletion(call):
    bot.edit_message_text(
        "O'chiriladigan kanalni tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=generate_delete_buttons()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_selected_channel(call):
    channel_id = int(call.data.split("_")[1])
    delete_channel(channel_id)
    bot.edit_message_text(
        "✅ Kanal muvaffaqiyatli o'chirildi!",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=generate_admin_panel()
    )

@bot.callback_query_handler(func=lambda call: call.data == "back_to_admin")
def back_to_admin_panel(call):
    channel_management(call.message)


#kodli qidiruv tugadi

@bot.message_handler(func=lambda message: message.text.isdigit())
def serial_search(msg):
    cid = msg.chat.id
    reply_to_user_id = msg.reply_to_message.from_user.id if msg.reply_to_message else None
    serial_id = int(msg.text)

    # Group yoki supergroupdagi xabar
    if msg.chat.type in ['group', 'supergroup']:
        # Database'da serial mavjudligini tekshirish
        serial = cursor.execute("SELECT * FROM serial WHERE id=?", (serial_id,)).fetchone()
        
        if serial:
            # Serial topilganda nomi va rasmi bilan yuborish
            name = serial[1]
            image = serial[2]  # Serialning rasmi (URL yoki path)
            btn = InlineKeyboardMarkup(row_width=1)
            btn.add(InlineKeyboardButton(text="👀 Tomosha qilish", url=f"https://t.me/pymovibot?start=s{serial_id}"))
            
            # Serialning rasmi va nomi bilan yuborish
            bot.send_photo(cid, photo=image, caption=f"<b>[✨] : {name}</b>", reply_markup=btn,reply_to_message_id=msg.reply_to_message.message_id if reply_to_user_id else msg.message_id)
        # Agar serial topilmasa, hech qanday javob bermaslik
        else:
            return
    # Private chat uchun
    elif msg.chat.type == 'private':
        # Private chatda botga qo'shilganligini tekshirish
        if not join(cid):
            return

        # Database'da serial mavjudligini tekshirish
        serial = cursor.execute("SELECT * FROM serial WHERE id=?", (serial_id,)).fetchone()

        if serial:
            name = serial[1]
            json = cursor.execute(f"SELECT * FROM movies WHERE serial='{name}'").fetchall()
            c = 0
            key = InlineKeyboardMarkup(row_width=4)
            m = []
            for i in json:
                c += 1
                m.append(InlineKeyboardButton(text=f"{c}", callback_data=f'yukla-{i[0]}'))
            key.add(*m)
            bot.delete_message(cid, msg.message_id)
            sent = bot.send_photo(cid, photo=serial[2], caption=f"<b>[✨] : {name} \n\n🎬 Qisimlar: {len(json)}</b>", reply_markup=key)
            bot.pin_chat_message(cid, sent.message_id)
        else:
            bot.reply_to(msg, f"""
😢 <code>{serial_id}</code><b> kodga tegshli film topilmadi 😢
Boshqa kodni yoki film nomini kiritib ko'ring...</b>""", reply_markup=main_btn())












# .terms buyrug'i
@bot.message_handler(commands=['terms'])
@only_owner
def send_terms(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        terms_text = grmsg

        # Gruhda reply qilish va foydalanuvchini mute qilish
        bot.reply_to(message.reply_to_message, "Sizga shartlar yuborildi. Shaxsiy chatda ularni qabul qilishingiz kerak.")
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

        # Shaxsiy chatda shartlarni yuborish
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Agree", callback_data=f"agree_{chat_id}_{user_id}")
        markup.add(button)
        bot.send_message(user_id, terms_text, reply_markup=markup)
    else:
        bot.reply_to(message, "Iltimos, foydalanuvchiga reply qiling.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("agree_"))
def agree_terms(call):
    data = call.data.split("_")
    chat_id = int(data[1])
    user_id = int(data[2])
    bot.send_message(chat_id, "Foydalanuvchi shartlarga rozi bo'ldi.")
    bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
    bot.send_message(user_id, "Shartlarga rozilik bildirdingiz. Endi gruhda yozishingiz mumkin.")



# group funksyasi
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_members(message):
    for new_member in message.new_chat_members:
        bot.send_message(new_member.id, grmsg,reply_markup=group_btn())

        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)




# Xabarni o'chirish uchun yordamchi funksiya
def delete_message_later(chat_id, message_id, delay=5):
    time.sleep(delay)  # Belgilangan vaqt kutish
    try:
        bot.delete_message(chat_id, message_id)
    except telebot.apihelper.ApiException:
        pass  # Xabar o'chirilgan bo'lsa, xatoni inkor qilish

@bot.message_handler(func=lambda message: message.text and message.text.startswith('/qidiruv'))
def janr_search(msg):
    cid = msg.chat.id
    reply_to_user_id = msg.reply_to_message.from_user.id if msg.reply_to_message else None

    if len(msg.text.split()) > 1:
        series_name = msg.text.replace('/qidiruv', '', 1).strip().lower()

        # Bazadan mos natijalarni olish
        relevant_serials = cursor.execute(
            "SELECT id, name FROM serial WHERE name LIKE ?", ('%' + series_name + '%',)
        ).fetchall()

        if relevant_serials:
            # Javob matni
            response_text = "*🔍 Qidiruv natijalari:*\n\n"
            for index, serial in enumerate(relevant_serials[:8], start=1):  # Max 8 ta natija
                serial_id, serial_name = serial
                serial_link = f"https://t.me/pymovibot?start=s{serial_id}"  # Serial havolasi
                response_text += f"{index}» [{serial_name[:30]}]({serial_link})\n"  # Havola qo'shildi

            # Inline tugmalar
            markup = telebot.types.InlineKeyboardMarkup(row_width=3)  # 3 ta tugma bir qatorda
            buttons = [
                telebot.types.InlineKeyboardButton(
                    text=f"{index} ✨",
                    url=f"https://t.me/pymovibot?start=s{serial[0]}"  # Serial ID bilan URL
                )
                for index, serial in enumerate(relevant_serials[:8], start=1)
            ]
            markup.add(*buttons)  # Tugmalarni qo'shish

            # Inline mode uchun tugma (eng ostida bo'ladi)
            inline_button = telebot.types.InlineKeyboardButton(
                text="🔍 Inline rejimda qidirish",
                switch_inline_query=""
            )
            markup.add(inline_button)

            # Xabarni yuborish
            sent_message = bot.send_photo(
                cid,
                photo="https://telegra.ph/file/b606eb049d503c5d3d2fc.jpg",  # Rasm URL
                caption=response_text,
                parse_mode="Markdown",  # Markdown formatda yuborish
                reply_markup=markup,
                reply_to_message_id=msg.reply_to_message.message_id if reply_to_user_id else msg.message_id
            )

        else:
            # Qidiruv topilmasa, javob yuborish
            warning_message = bot.send_message(
                cid,
                "Afsus, siz izlagan serial topilmadi.",
                reply_to_message_id=msg.reply_to_message.message_id if reply_to_user_id else msg.message_id
            )
            # Xabarni 5 sekunddan so'ng o'chirish
            threading.Thread(target=delete_message_later, args=(cid, warning_message.message_id)).start()

    else:
        # Foydalanuvchi noto'g'ri formatda qidiruv yuborgan bo'lsa
        info_message = bot.send_message(
            cid,
            "Qidiruv buyrug'idan so'ng matn kiriting: /qidiruv yozgi tunel",
            parse_mode="Markdown",
            reply_to_message_id=msg.reply_to_message.message_id if reply_to_user_id else msg.message_id
        )
        # Xabarni 5 sekunddan so'ng o'chirish
        threading.Thread(target=delete_message_later, args=(cid, info_message.message_id)).start()







# inline rejim
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(inline_query):
    try:
        query = inline_query.query
        search_results = search_series(query)
        if not search_results:
            bot.answer_inline_query(inline_query.id, [
                telebot.types.InlineQueryResultArticle(

                  id='0',
                    title='📛 Siz izlagan film topilmadi',
                    input_message_content=telebot.types.InputTextMessageContent(message_text="📛 Kino topilmadi.")
                )
            ])
        else:
            results = [
                telebot.types.InlineQueryResultArticle(
                    id=str(series['id']),
                    title=series['name'],
                    input_message_content=telebot.types.InputTextMessageContent(message_text=f"""

<b>🔍 ɪɴʟɪɴᴇ ǫɪᴅᴜʀᴜᴠ ɴᴀᴛɪᴊᴀsɪ:

ᴋɪɴᴏ ɴᴏᴍɪ :</b><code> {series['name']} </code>

<a href="https://envs.sh/ow8.jpg">&#8288;</a>"""
                  ,parse_mode="html"),
                    reply_markup=telebot.types.InlineKeyboardMarkup().add(
                      telebot.types.InlineKeyboardButton(
                          text="👀ᴛᴏᴍᴏsʜᴀ ǫʟɪsʜ",
                          url=f"https://t.me/pymovibot?start=s{series['id']}"
                      )
                      ).row(
                      telebot.types.InlineKeyboardButton(
                          text="🔍ǫɪᴅɪʀɪsʜ",
                        switch_inline_query=""  # Bu qayta urinish tugmasi
                      )
                    )
                  )
                for series in search_results
            ]
            bot.answer_inline_query(inline_query.id, results)
    except Exception as e:
        print(e)
# inline rejim tugadi





@bot.message_handler(content_types=['video'])
def add_video(msg):
    if msg.chat.id in ADMIN_ID:
        cid = msg.chat.id
        file_id = msg.video.file_id
        caption = msg.caption

        # File ID va Caption saqlash
        FILE_ID['id'] = file_id
        CAPTION['text'] = caption

        # Seriallar sonini aniqlash
        total_serials = len(cursor.execute("SELECT * FROM serial").fetchall())
        total_pages = (total_serials - 1) // 20 + 1  # Har bir sahifada 20 ta serial

        # Birinchi sahifani ko'rsatish
        show_serials_page(cid, 1, total_pages)


def show_serials_page(chat_id, page, total_pages, message_id=None):
    page_size = 20  # Sahifada ko'rsatiladigan seriallar soni
    start_index = (page - 1) * page_size

    # Seriallarni teskari tartibda olib kelish
    serials_on_page = cursor.execute(
        "SELECT * FROM serial ORDER BY id DESC LIMIT ? OFFSET ?",
        (page_size, start_index)
    ).fetchall()

    # Klaviatura yaratish
    key = InlineKeyboardMarkup()

    # Sahifadagi seriallar uchun tugmalar
    for serial in serials_on_page:
        key.add(InlineKeyboardButton(text=f"{serial[1]}", callback_data=f"newserial-{serial[0]}"))

    # Sahifa tugmalari
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page-{page - 1}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"page-{page + 1}"))

    if navigation_buttons:
        key.add(*navigation_buttons)

    # Xabarni jo'natish yoki yangilash
    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"📄 Sahifa {page}/{total_pages}\nSerialni tanlang:",
            reply_markup=key
        )
    else:
        bot.send_message(
            chat_id,
            f"📄 Sahifa {page}/{total_pages}\nSerialni tanlang:",
            reply_markup=key
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("page-"))
def handle_page_change(call):
    cid = call.message.chat.id
    mid = call.message.id
    page = int(call.data.split('-')[1])

    # Umumiy sahifalar sonini aniqlash
    total_serials = len(cursor.execute("SELECT * FROM serial").fetchall())
    total_pages = (total_serials - 1) // 20 + 1

    # Sahifani yangilash
    show_serials_page(cid, page, total_pages, message_id=mid)



@bot.message_handler(content_types=['text'])
def custom(msg):
  cid = msg.chat.id
  text = msg.text
  if text=='/panel' and cid in ADMIN_ID:
    bot.reply_to(msg,"<b>Admin panelga xush kelibsiz!</b>",reply_markup=admin_panel())
  try:
    if text=="📊 Statistika":
      try:
        count_serial = cursor.execute("SELECT COUNT(id) FROM serial").fetchone()[0]
        count_movie = cursor.execute("SELECT COUNT(id) FROM movies").fetchone()[0]      
        users = cursor.execute("SELECT COUNT(id) FROM users").fetchone()[0]
        kino = cursor.execute("SELECT COUNT(id) FROM kino").fetchone()[0]
        txt = f"""<b>
Bot statistikasi 📊

👤 Obunachilar: {users} ta  

📺 Seriallar: {count_serial} ta
🎬 Serial qismi: {count_movie} ta

</b>
      """
        bot.send_message(cid,txt)
      except Exception as e:
        print(e)


    if text=="✉ Oddiy xabar" and cid in ADMIN_ID:
      a = bot.send_message(cid,"<b>Xabar matnini kiriting: </b>")
      bot.register_next_step_handler(a,oddiy_xabar)
    elif text=="✉ Forward xabar" and cid in ADMIN_ID:
      a = bot.send_message(cid,"<b>Xabar matnini yuboring: </b>")
      bot.register_next_step_handler(a,forward_xabar)
    elif text=="➕ Serial qo'shish" and cid in ADMIN_ID:
      a = bot.send_message(cid,"<b>Seryal nomini yuboring!</b>")
      bot.register_next_step_handler(a,new_serial)       
    elif text=="📺 Seriallar" and cid in ADMIN_ID:
      total_serials = len(cursor.execute("SELECT * FROM serial").fetchall())

      # Sahifalash
      page_size = 40  # Har bir sahifadagi elementlar soni
      total_pages = (total_serials - 1) // page_size + 1  # Umumiy sahifalar soni

      # Sahifalarni chiqarish
      for page_number in range(1, total_pages + 1):
          start_index = (page_number - 1) * page_size
          end_index = min(page_number * page_size, total_serials)
          serials_on_page = cursor.execute("SELECT * FROM serial LIMIT ? OFFSET ?", (page_size, start_index)).fetchall()

          # Yangi klaviatura yaratish
          key = InlineKeyboardMarkup()

          # Sahifadagi har bir serial uchun tugmalar
          for serial in serials_on_page:
              key.add(InlineKeyboardButton(text=f"{serial[1]}", callback_data=f"info-{serial[0]}"))

          # Agar keyingi sahifa mavjud bo'lsa, "Keyingi sahifa" tugmasini qo'shish
          if page_number < total_pages:
              key.add(InlineKeyboardButton(text="Davomi ⬇️", callback_data=f"next_page-{page_number + 1}"))

          # Xabarni jo'natish
          bot.reply_to(msg, "Serial nomini tanlanag!", reply_markup=key)
  except:
    pass


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
  cid = call.message.chat.id
  mid = call.message.id
  data = call.data
  if data=="member":
    if data == "member":
        if join(cid):
            bot.edit_message_text(
                """
<b>🙂 Barcha kanallarga obuna bo'ldingiz</b>

<i>Menga shunchali Film kodini yoki nomini yuboring yoki Bosh menyuga o'ting </i>""",
                chat_id=cid,  
                message_id=mid,
                reply_markup=main_btn()
            )
        else:
            bot.answer_callback_query(
                call.id,
                "❌ Hali ham barcha kanalga  a'zo bo'lmadingiz. Iltimos, barcha kanallarga a'zo bo'ling!",
                show_alert=True
            )


  if data=='solo':
    try:
      file_id = FILE_ID['id']
      caption =CAPTION['text'].replace("'","||")
      all = cursor.execute("SELECT * FROM kino").fetchall()
      if len(all)==0:
        code = 1
      else:
        code = all[-1][0]+1
      cursor.execute(f"INSERT INTO kino(file_id,caption) VALUES('{file_id}','{caption}')")
      bot.send_video(cid,video=file_id,caption=caption.replace("||","'"),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="📥 Yuklab olish",url=f"https://t.me/Pymovibot?start=f{code}")))

    except Exception as e:
      print(e)
  elif "serial" in data:
    id  = data.split("-")[1]
    bot.delete_message(cid,mid)
    file_id = FILE_ID['id']
    caption =CAPTION['text'].replace("'","||")
    all = cursor.execute("SELECT * FROM movies").fetchall()
    if len(all)==0:
      code = 1
    else:
      code = all[-1][0]+1
    serial = cursor.execute(f"SELECT * FROM serial WHERE id={id}").fetchone()[1]
    cursor.execute(f"INSERT INTO movies(file_id,caption,serial) VALUES('{file_id}','{caption}','{serial}')")
    bot.send_video(cid,video=file_id,caption=caption.replace("||","'"),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="📥 Yuklab olish",url=f"https://t.me/Pymovibot?start=s{id}")))

  elif "yukla" in data:
    data = call.data.split("-")[1]
    json = cursor.execute(f"SELECT * FROM movies WHERE id={data}").fetchone()
    cid = call.message.chat.id

    # Video yuborish
    bot.send_video(cid, video=json[1], caption=json[2].replace("||", "'"), protect_content=True)

  
  elif "info" in data:
    id  = data.split("-")[1]
    json = cursor.execute(f"SELECT * FROM serial WHERE id={id}").fetchone()
    get = cursor.execute(F"SELECT * FROM movies WHERE serial='{json[1]}'").fetchall()
    c = 0
    key = InlineKeyboardMarkup(row_width=4)
    m = []
    for i in get:
      c+=1
      m.append(InlineKeyboardButton(text=f"🗑 {c}",callback_data=f'del-{i[0]}'))
    key.add(*m)
    key.add(InlineKeyboardButton(text=f"❌ Serial",callback_data=f'remove-{id}'),InlineKeyboardButton(text=f"Post share",callback_data=f'share-{id}'))
    bot.send_photo(cid,photo=json[2],caption=f"<b>🎥 Serial: {json[1]}\n📥 Yuklash: https://t.me/Pymovibot?start=s{id}\n🎬 Qisimlar: {c}\nkanal : @pymoviee</b>",reply_markup=key)
  elif "del" in data:
    id  = data.split("-")[1]
    bot.delete_message(cid,mid)
    cursor.execute(f"DELETE FROM movies WHERE id={id}")
    js = cursor.execute("SELECT * FROM serial").fetchall()
    key = InlineKeyboardMarkup()
    for i in js:
      key.add(InlineKeyboardButton(text=f"{i[1]}",callback_data=f"info-{i[0]}"))
    bot.send_message(cid,"<b>❌ Serial qismi o'chirildi!</b>",reply_markup=key)
  elif "remove" in data:
    id  = data.split("-")[1]
    bot.delete_message(cid,mid)
    cursor.execute(f"DELETE FROM serial WHERE id={id}")
    conn.commit()
    js = cursor.execute("SELECT * FROM serial").fetchall()
    key = InlineKeyboardMarkup()
    for i in js:
      key.add(InlineKeyboardButton(text=f"{i[1]}",callback_data=f"info-{i[0]}"))
    bot.send_message(cid,"<b>❌ Serial o'chirildi!</b>",reply_markup=key)


  elif "share" in data:
      id  = data.split("-")[1]
      js = cursor.execute(F"SELECT * FROM serial WHERE id={id}").fetchall()

      channel_id = -1001840747143  # Kanal identifikatori (negative qiymat)
      bot.send_chat_action(cid, 'upload_photo')  # Yuborish jarayonini bildirish
      bot.send_photo(channel_id, photo=js[0][2], caption=f"""
❄️ *Bugungi Kino Tavsiyamiz*
[─────────](https://t.me/Pymovibot?start=s{id})
🎬 *Kino nomi* » `{js[0][1]}`
🎦 *Film kodi* » `{js[0][0]}`
[─────────](https://t.me/Pymovibot?start=s{id})

✨ pymovie.uz | [pymovie channel](t.me/pymoviee) | [pymovie bot](t.me/pymovibot) | [instagram](https://www.instagram.com/pymovie?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==) | [pyfot](t.me/pyfot)""",reply_markup=InlineKeyboardMarkup().add(
                  InlineKeyboardButton(text="📥 ʏᴜᴋʟᴀʙ ᴏʟɪꜱʜ", url=f"https://t.me/Pymovibot?start=s{id}")).add(InlineKeyboardButton(text="🎬 Treyler ", callback_data='trailer')), parse_mode='Markdown')
      bot.delete_message(cid,mid)
      bot.send_message(cid,"<b>✅ Post kanalga yuborildi!</b>")
      time.sleep(4)
      bot.delete_message(cid,mid+1)


def start_bot():
  try:
      bot.polling(none_stop=True)
      time.sleep(60)
  except Exception as e:
      bot.send_message(ADMIN_ID[0], f"""
Xatolik

<code>{e}</code>""")
      print(e)
      traceback.print_exc()
      start_bot()  # Botni qayta ishga tushurish

# Botni ishga tushurish
start_bot()

