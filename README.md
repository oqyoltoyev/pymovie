# PyMovie.UZ

`PyMovie` — bu Python dasturlash tilida yozilgan kino va seriallar botidir. Ushbu loyiha yordamida foydalanuvchilar o'zlariga kerakli kino yoki serialni qidirishi va ularga doir ma'lumotlarni osongina olishi mumkin.

## O'rnatish

Quyidagi qadamlarni bajarib, `PyMovie` botini o'z tizimingizga o'rnating:

1. **Loyihani klonlash:**
    ```bash
    git clone https://github.com/oqyoltoyev/pymovie.git
    cd pymovie
    ```

2. **Talab qilinadigan kutubxonalarni o'rnatish:**
    Loyihada foydalaniladigan barcha kutubxonalar `requirements.txt` faylida ko'rsatilgan:
    ```bash
    pip install -r requirements.txt
    ```

3. **Telegram Bot Tokenini sozlash:**
    Botingiz ishlashi uchun Telegram'dan olgan bot tokeningizni `.env` fayliga qo'shing:
    ```env
    BOT_TOKEN=your-telegram-bot-token
    ```

## Ishga tushirish

Botni ishga tushirish uchun quyidagi buyruqni bajaring:
```bash
python main.py
```

Agar bot muvaffaqiyatli ishga tushsa, u sizning Telegram hisobingizga ulanadi va buyruqlarga javob bera boshlaydi.

## Foydalanish

### Asosiy buyruqlar
Bot quyidagi asosiy buyruqlarni qo‘llab-quvvatlaydi:

- **/start** — Botdan foydalanishni boshlash.
- **inline buttonlar** — Yordamida to'liq boshqarvga ega va edit message orqali qulay navigatsiya bor



## Xususiyatlar

- **Tezkor qidiruv:** Kino va seriallarni nomi bo‘yicha tezda topadi.
- **To‘liq ma’lumot:** Har bir kino yoki serial uchun to‘liq ma’lumot (rejissor, janr, reyting) ko‘rsatiladi.
- **Yangiliklar:** So‘nggi chiqarilgan kinolar ro‘yxatini ko‘rish imkoniyati.

## Loyihaga hissa qo‘shish

Agar siz loyiha rivojlanishiga o‘z hissangizni qo‘shmoqchi bo‘lsangiz, pull request yuborishingiz yoki issue yaratishingiz mumkin. Hissangizni qadrlaymiz!

1. **Fork qiling:**
    ```bash
    git fork https://github.com/username/pymovie.git
    ```

2. **O‘zgarishlar kiriting va commit qiling:**
    ```bash
    git commit -m "Qo'shimcha xususiyat qo'shildi"
    ```

3. **Pull request yuboring.**

## Litsenziya

Ushbu loyiha [MIT litsenziyasi](LICENSE) asosida tarqatiladi.
