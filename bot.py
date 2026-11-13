import telebot
from telebot import types

# Данные вашего бота (Уже заполнены!)
BOT_TOKEN = "9035255606:AAEz8CZZh7y5UOEEcl76-R948hyjxMjRHr4"
ADMIN_SETS = "evolution_12"   # Для продажи сетов
ADMIN_SOPR = "Sin20014"       # Для сопровождения

bot = telebot.TeleBot(BOT_TOKEN)

# Главное меню
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_shop = types.InlineKeyboardButton("🛒 Каталог товаров", callback_data="open_shop")
    btn_profile = types.InlineKeyboardButton("👤 Мой профиль", callback_data="open_profile")
    btn_reviews = types.InlineKeyboardButton("⭐ Отзывы", callback_data="open_reviews")
    btn_support = types.InlineKeyboardButton("👨‍💻 Поддержка", callback_data="open_support")
    markup.add(btn_shop, btn_profile, btn_reviews, btn_support)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Добро пожаловать в **SIN METRO SHOP**! 🛒\n\n"
        "Здесь ты можешь купить топовые сеты брони и заказать профессиональное сопровождение (вынос лута) с гарантией!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="🤖 Главное меню Metro Shop:", reply_markup=main_menu())
        
    elif call.data == "open_shop":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_sets = types.InlineKeyboardButton("🎒 Сеты (Броня/Оружие)", callback_data="cat_sets")
        btn_sopr = types.InlineKeyboardButton("🗺️ Сопровождение (Вынос)", callback_data="cat_sopr")
        btn_back = types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
        markup.add(btn_sets, btn_sopr, btn_back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="📦 **Выберите категорию товаров:**", reply_markup=markup, parse_mode="Markdown")

    # Вкладка: Сеты
    elif call.data == "cat_sets":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_buy_set1 = types.InlineKeyboardButton("🎒 Фул 6 + МК + ВК — 100 руб.", callback_data="buy_set_full6")
        btn_back = types.InlineKeyboardButton("⬅️ Назад в категории", callback_data="open_shop")
        markup.add(btn_buy_set1, btn_back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="🎒 **Доступные комплекты (Сеты):**\n\nВыбирайте нужный товар:", reply_markup=markup, parse_mode="Markdown")

    # Вкладка: Сопровождение (ТЕПЕРЬ 10 ТАРИФОВ)
    elif call.data == "cat_sopr":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_s1 = types.InlineKeyboardButton("🗺️ Спр 7карта (вынос 5-11м + шмот) — 150 руб.", callback_data="buy_sopr_7_short")
        btn_s2 = types.InlineKeyboardButton("🗺️ Спр 7карта (вынос 7-15м + шмот) — 230 руб.", callback_data="buy_sopr_7_long")
        btn_s3 = types.InlineKeyboardButton("💎 Спр 7карта (вынос 10-20м + шмот) — 550 руб.", callback_data="buy_sopr_7_max")
        
        # --- НОВЫЕ ТОВАРЫ ДЛЯ 7 КАРТЫ С ГАРАНТОМ ---
        btn_s4 = types.InlineKeyboardButton("🎫 Спр 7карта (Гарант 9л + шмот) — 350 руб.", callback_data="buy_sopr_7_g9")
        btn_s5 = types.InlineKeyboardButton("⚡ Спр 7карта (Гарант 15л + шмот) — 660 руб.", callback_data="buy_sopr_7_g15")
        
        btn_s6 = types.InlineKeyboardButton("🗺️ Сопр 7-8карта (вынос 7-20м + шмот) — 320 руб.", callback_data="buy_sopr_78")
        btn_s7 = types.InlineKeyboardButton("🎫 Спр 8карта (вынос 10-20м + шмот + Гарант 8 бил) — 400 руб.", callback_data="buy_sopr_8_classic")
        btn_s8 = types.InlineKeyboardButton("🔥 Спр 8карта (вынос 10-25м + шмот + Гарант 12 бил) — 450 руб.", callback_data="buy_sopr_8_medium")
        btn_s9 = types.InlineKeyboardButton("👑 Спр 8карта (вынос 20-35м + шмот + Гарант 16 бил) — 1000 руб.", callback_data="buy_sopr_8_hard")
        btn_s10 = types.InlineKeyboardButton("🔱 Сопр 7-8карта (вынос 25-45м + шмот) — 2000 руб.", callback_data="buy_sopr_78_vip")
        
        btn_back = types.InlineKeyboardButton("⬅️ Назад в категории", callback_data="open_shop")
        markup.add(btn_s1, btn_s2, btn_s3, btn_s4, btn_s5, btn_s6, btn_s7, btn_s8, btn_s9, btn_s10, btn_back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="🗺️ **Услуги сопровождения (Сопроводы):**\n\nВынос лута со шмотом и гарантиями по билетам/лимонам:", reply_markup=markup, parse_mode="Markdown")

    # Оформление заказа
    elif call.data.startswith("buy_"):
        item_code = call.data.replace("buy_", "")
        
        items_dict = {
            "set_full6": "🎒 Фул 6 сет с МК и ВК (Цена: 100 руб.)",
            "sopr_7_short": "🗺️ Сопровождение на 7 карту [вынос от 5-11м + шмот] (Цена: 150 руб.)",
            "sopr_7_long": "🗺️ Сопровождение на 7 карту [вынос от 7-15м + шмот] (Цена: 230 руб.)",
            "sopr_7_max": "💎 Топ-Сопровождение на 7 карту [вынос от 10-20м + шмот] (Цена: 550 руб.)",
            # Новые позиции:
            "sopr_7_g9": "🎫 Сопровождение на 7 карту [Гарант 9 лимонов + шмот] (Цена: 350 руб.)",
            "sopr_7_g15": "⚡ Сопровождение на 7 карту [Гарант 15 лимонов + шмот] (Цена: 660 руб.)",
            
            "sopr_78": "🗺️ Сопровождение 7-8 карта [вынос 7-20м + шмот] (Цена: 320 руб.)",
            "sopr_8_classic": "🎫 Сопровождение на 8 карту [вынос от 10-20м + шмот + гарант 8 билетов] (Цена: 400 руб.)",
            "sopr_8_medium": "🔥 Сопровождение на 8 карту [вынос от 10-25м + шмот + гарант 12 билетов] (Цена: 450 руб.)",
            "sopr_8_hard": "👑 VIP-Сопровождение на 8 карту [вынос от 20-35м + шмот + гарант 16 билетов] (Цена: 1000 руб.)",
            "sopr_78_vip": "🔱 ЭЛИТНОЕ Сопровождение 7-8 карта [вынос от 25-45м + шмот] (Цена: 2000 руб.)"
        }
        
        selected_item = items_dict.get(item_code, "Выбранный товар")
        
        if "set" in item_code:
            target_admin = ADMIN_SETS
        else:
            target_admin = ADMIN_SOPR
            
        markup = types.InlineKeyboardMarkup()
        btn_admin = types.InlineKeyboardButton("📱 Оформить у Продавца", url=f"t.me/{target_admin}")
        btn_back = types.InlineKeyboardButton("⬅️ В магазин", callback_data="open_shop")
        markup.add(btn_admin, btn_back)
        
        order_text = (
            f"🛒 **Вы выбрали:**\n{selected_item}\n\n"
            "Чтобы совершить покупку, произвести оплату и договориться о времени, "
            "нажмите кнопку ниже и напишите нашему продавцу."
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=order_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "open_profile":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
        profile_text = f"👤 **Ваш профиль в SIN METRO SHOP:**\n\n🆔 ТГ-ID: `{call.from_user.id}`\n🔑 Имя: {call.from_user.first_name}\n🎒 Всего заказов: 0"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=profile_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "open_reviews":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Открыть канал с отзывами", url="https://t.me"))
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="⭐ **Гарантии и Отзывы:**\n\nМы работаем честно и быстро! Все отзывы наших покупателей вы можете посмотреть по ссылке ниже.", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "open_support":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("👨‍💻 Написать главному админу", url=f"t.me/{ADMIN_SOPR}"))
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text="👨‍💻 Возникли вопросы или проблемы? Напишите администрации напрямую.", reply_markup=markup)

bot.polling(none_stop=True)
