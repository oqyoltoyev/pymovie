#config.py | kutubxonalar
import telebot
from telebot.types import *
from pymovie.config import *
from datetime import datetime, timedelta
from telebot.types import Message , InlineKeyboardMarkup, InlineKeyboardButton , ChatPermissions
from telebot.types import Message
from telebot import types
from rapidfuzz import process, fuzz
import time
from pymovie.database import *
# kutubxonalar tugadi

# vaqtinchalik xotira
NEW_SERIAL = {}
CAPTION = {}
FILE_ID = {}
# vaqtinchalik xotira tugadi



# Admin o'zgaruvchilari
ADMIN_ID = [5921733345,6325574205 ,1739407678, 6699875416,5760452570,6845147329]
# Admin o'zgaruvchilari tugadi

OWNER_ID = ADMIN_ID[0]

#token
token = "6459135662:AAG4h2rVTkeglOf77aEFWyvI0IbnpIIwcJQ"
bot = telebot.TeleBot(token,parse_mode='html')
#token tugadi

# shorts bo'limi



dub_text=f"""
<b>🛑 Qoidalarni o'qib chqing  🛑

1) Yoshi 16-17 dan oshgan bo'lishi kerak
2) Dublyaj qilish bo'yicha tushunchasi bo'lishi kerak
3) Shevada gapirmasligi kerak
4) Iloji boricha chet tilini bilishi kerak (shart emas)
5) Berilgan topshiriqni vaqtida bajarib o'z ishiga puxta yondashish kerak
6) Boshqa fan dublarda ishlamasligi shart</b>

<blockquote>Qoidalarga rozi bo'lsangiz tugmani bosing</blockquote>"""

dub2_text= f"""<b>
🖊 Endi esa Ismingiz yoshingiz va tajribangiz haqida adminga yozing
</b>
<blockquote>🚫 Muomilasi yoqlar spam bo'ladi</blockquote>"""

admin_text=f"""
👮🏻‍♀️ Adminlik turlari :

1) Kanalga edit va qiziqarli post tashlash,
2) Botga Film yuklash uchun ,
3) Gruhda saavollarga javob berish ,
4) Anime , Dorama , Kino topish uchun
5) Pymovie instgarmi uchun

<blockquote>Bu eng masulyatli ishlar</blockquote>"""

def private_chat_only(func):
  def wrapper(message: Message):
      if message.chat.type == 'private':
          return func(message)
      else:
          bot.reply_to(message, "🙁 Bu funksya faqat @pymovibot chatida ishlaydi\n<blockquote> Botni gruhda ishlatguncha miyyani ishlating 😢</blockquote>")
  return wrapper



# Buttonlar hammasi . . .

def adminga():
  key = InlineKeyboardMarkup()
  key.add(InlineKeyboardButton(text="Admin bo'lmoqchiman", url="t.me/pyfotuz"))
  return key

def dub_btn():
  btn = InlineKeyboardMarkup()
  btn.add(InlineKeyboardButton(text="📝 Yozish", url="http://t.me/pyfotuz?text=🍃Assalomualaykum%20men%20Dublyaj%20gruhga%20qoshilmoqchiman"))
  return btn


def group_btn():
  btn = InlineKeyboardMarkup(row_width=2)
  btn.add(InlineKeyboardButton(text="Pymovie Group", url="t.me/pymovie_group"))
  return btn

def main_btn():
    btn = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="🪼 Kanalimiz",url='t.me/pymoviee')
    b2 = InlineKeyboardButton(text="⌂ Home", callback_data='home')
    btn.row(b1,b2)
    return btn
# start buttonlar

def main_menu():
    btn = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton(text="🧩 Web ilova",web_app=types.WebAppInfo(url='https://pymovie.uz'))
    b2 = InlineKeyboardButton(text="🔍 Film qidirish", switch_inline_query_current_chat="")
    b3 = InlineKeyboardButton(text="📣 E'lonlar", callback_data='news')
    b4 = InlineKeyboardButton(text="ℹ️ Qo'llanma", web_app=types.WebAppInfo(url='https://pult.serv00.net/'))
    b5 = InlineKeyboardButton(text="»»»", callback_data='next_page')
    btn.add(b1, b2)
    btn.add(b3, b4)
    btn.add(b5)
    return btn


# admin panel reply keyboard
def admin_panel():
  key = ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder='Admin paneli')
  key.add(
    KeyboardButton("📺 Seriallar"),
    KeyboardButton("➕ Serial qo'shish"))
  key.add(
    KeyboardButton("✉ Oddiy xabar"),
    KeyboardButton("✉ Forward xabar"),
  )
  key.add(
      KeyboardButton("📊 Statistika"),
      KeyboardButton("📣 E'lonlar")
  )
  key.add(
      KeyboardButton("🎴 Kanallarni boshqarish")
  )
  return key

# Barcha buttonlar tugadi . . .

# group funksyasi for text
grmsg = """
 @pymovie_groupga<b> ɢᴀ ǫᴏ'sʜɪʟᴅɪɴɢɪᴢ ✅:

 ▫️ ɢᴜʀᴜʜɢᴀ ʜᴀʀ xɪʟ ʀᴇᴋʟᴀᴍᴀʟᴀʀ ʀᴇғᴇʀᴀʟ ʜᴀᴠᴏʟᴀʟᴀʀ ʏᴜʙᴏʀᴍᴀɴɢ !

 ▫️ ᴏʀᴛɪǫᴄʜᴀ ᴄʜᴀᴛ ǫɪʟᴍᴀɴɢ ғᴀǫᴀᴛ ᴋᴇʀᴀᴋʟɪ ʜᴀʙᴀʀ ʏᴏᴢɪɴɢ !

 ▫️ ʙɪʀ ʙɪʀɪɴɢɪᴢɴɪ ʜᴜʀᴍᴀᴛ ǫʟɪɴɢ !

📛 ʏᴜǫᴏʀɪᴅᴀɢɪ ǫᴏʏᴅᴀʟᴀʀᴅᴀɴ ʙɪʀɪɴɪ ʙᴜᴢsᴀɴɢɪᴢ ʙʟᴏᴋ ʏᴏᴋɪ ᴍᴜᴛᴇ ǫɪʟɪɴᴀsɪᴢ</b>
"""

# seaarial qo'shish funksyasi
def new_serial(msg):
  try:
    cid = msg.chat.id
    try:
      file_id = msg.photo[-1].file_id
      text = msg.caption.replace("'","'")
    except:  
      pass
    if msg.text=="Cancel":
      bot.reply_to(msg,"<b>Bekor qilindi!</b>",reply_markup=admin_panel())
    else:
      cursor.execute(f"INSERT INTO serial(name,file_id) VALUES('{text}','{file_id}')")
      conn.commit()
      bot.send_photo(cid,file_id,caption="<b>✅ Yangi serial qoshildi!</b>",reply_markup=admin_panel())
  except Exception  as e:
    print(e)


def search_series(series_name):
    cursor = conn.cursor()

    # Bazadan barcha serial nomlari va ularning IDlarini olish
    cursor.execute("SELECT id, name FROM serial")
    all_series = cursor.fetchall()
    series_dict = {row[1]: row[0] for row in all_series}

    # Fuzzy qidiruv (ancha aniqroq uchun partial_ratio ishlatamiz)
    matches = process.extract(series_name, series_dict.keys(), limit=10, scorer=fuzz.partial_ratio)

    # Natijalarni to'plash va qaytarish
    results = [
        {'id': series_dict[match[0]], 'name': match[0], 'score': match[1]} for match in matches if match[1] > 60
    ]

    # Agar aniq natijalar bo'lmasa, bo'sh natija qaytaramiz
    return sorted(results, key=lambda x: x['score'], reverse=True) if results else [{'id': None, 'name': 'No match found', 'score': 0}]

def oddiy_xabar(msg):
    success = 0
    error = 0
    
    # Ma'lumotlar bazasidan foydalanuvchilar ro'yxatini olish
    stat = cursor.execute("SELECT chat_id FROM users").fetchall()
    
    for user in stat:
        chat_id = user[0]
        try:
            # Xabarni nusxalab yuborish
            bot.copy_message(chat_id=chat_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
            success += 1
            
            # Flood limitni oldini olish uchun kutish
            time.sleep(0.5)  # Har xabar orasida yarim soniya kutish
        except Exception as e:
            print(f"Xatolik {chat_id} ga yuborishda: {e}")
            error += 1
            
            # Retry (qayta urinish) qilishga harakat
            time.sleep(2)
            try:
                bot.copy_message(chat_id=chat_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
                success += 1
                error -= 1  # Xatoni tuzatilgan deb hisoblash
            except Exception as retry_error:
                print(f"Qayta urinish muvaffaqiyatsiz {chat_id} uchun: {retry_error}")
    
    # Adminlarga natijalarni yuborish
    for admin_id in ADMIN_ID:
        bot.send_message(
            admin_id,
            f"<b>Xabar yuborildi!</b>\n\n✅ Yuborildi: {success}\n❌ Yuborilmadi: {error}",
            parse_mode='HTML'
        )

def forward_xabar(msg):
  success = 0
  error = 0
  stat = cursor.execute("SELECT chat_id FROM users").fetchall()
  for i in stat:
    print(i[0])
    try:
      success+=1
      bot.forward_message(i[0], ADMIN_ID, msg.message_id)
    except:
      error+=1
  for chat_id in ADMIN_ID:
    bot.send_message(chat_id, f"<b>Xabar yuborildi!\n\n✅Yuborildi: {success}\n❌ Yuborilmadi: {error}</b>", reply_markup=admin_panel())



def generate_admin_panel():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()
    if channels:
        for channel in channels:
            keyboard.add(InlineKeyboardButton(f"{channel[1]} ({channel[2]})", callback_data="no_action"))
    else:
        keyboard.add(InlineKeyboardButton("❌ Kanallar mavjud emas.", callback_data="no_action"))
    keyboard.add(
        InlineKeyboardButton("➕ Kanal qo'shish", callback_data="add_channel"),
        InlineKeyboardButton("❌ Kanal o'chirish", callback_data="delete_channel")
    )
    return keyboard

def generate_delete_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()
    for channel in channels:
        keyboard.add(InlineKeyboardButton(channel[1], callback_data=f"delete_{channel[0]}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin"))
    return keyboard


def generate_join_key():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()  # Kanallarni databasedan olish
    for channel in channels:
        # Kanallar ma'lumotlarini to'g'ri indekslar bilan foydalanish
        keyboard.add(InlineKeyboardButton(channel[1], url=channel[2]))
    keyboard.add(InlineKeyboardButton('✅ Tasdiqlash', callback_data="member"))
    return keyboard
 

def join(user_id):
    channels = get_channels()  # Kanallar ro'yxati
    for channel in channels:
        try:
            channel_url = channel[2]  # Kanal URL'si https://t.me/cosmos_for formatida
            channel_username = channel_url.split('/')[-1]  # username: cosmos_for
            if not channel_username.startswith('@'):
                channel_username = '@' + channel_username  # @cosmos_for formatiga o'tkazish

            print(f"Kanal username: {channel_username}")

            member = bot.get_chat_member(channel_username, user_id)

            if member.status not in ['member', 'creator', 'administrator']:
                # Foydalanuvchi a'zo emas
                bot.send_message(
                    user_id,
                    "👋 <b>Assalomu alaykum!</b>\n\n"
                    "Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling va "
                    "'✅ Tasdiqlash' tugmasini bosing.",
                    parse_mode='HTML',
                    reply_markup=generate_join_key()  # Inline tugmalarni jo'natish
                )
                return False
        except Exception as e:
            # Xatolikni chop etish
            bot.send_message(
                OWNER_ID,
                f"Kanaldagi a'zolikni tekshirishda xatolik: {str(e)}. Iltimos, administrator bilan bog'laning."
            )
            return False

    # Foydalanuvchi barcha kanallarga a'zo
    return True
