import telebot
from telebot import types
import matplotlib.pyplot as plt
import numpy as np
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('6895022639:AAEZXb0NKvL2nhKr_16gL5o63zBodakDm_Y')

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """
Обработчик команды /start

Args:
- message (types.Message): Объект сообщения пользователя.
"""
    bot.reply_to(message, "Привет, я бот для решения экономических задач🤓. Используй кнопки для навигации‼❗️")
    
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button1 = types.KeyboardButton("Построение общей КПВ")
    button2 = types.KeyboardButton("Нахождение точки рыночного равновесия")
    button3 = types.KeyboardButton("Расчет объема дефицита/излишка")
    button4 = types.KeyboardButton("Расчет прибыли фирмы")
    
    keyboard.add(button1, button2, button3, button4)
    
    # Отправляем клавиатуру с сообщением
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=keyboard)

# Обработчик для остальных типов файлов
@bot.message_handler(content_types=[ 'sticker', 'location', 'contact', 'document', 'video', 'audio'])
def handle_other_types(message):
    """
    Обработчик для остальных типов файлов.

    В данной функции обрабатываются сообщения, содержащие файлы типа 'sticker', 'location', 'contact',
    'document', 'video' и 'audio'. Она отправляет пользователю сообщение о том, что обработка данного
    типа файла не поддерживается.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    bot.reply_to(message, "Извините, но обработка этого типа файла не поддерживается.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Обработчик для получения и обработки фотографии.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    try:
        photo = open('f.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при обработке изображения: {e}")

# Обработчик нажатия на кнопку "Нахождение точки рыночного равновесия"
@bot.message_handler(func=lambda message: message.text == "Нахождение точки рыночного равновесия", content_types=['text'])
def handle_market_equilibrium_start(message):
    """
    Обработчик нажатия на кнопку "Нахождение точки рыночного равновесия".

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    remove_keyboard = types.ReplyKeyboardRemove()

    # Клавиатура с кнопкой "Назад"
    back_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    back_keyboard.add(back_button)

    bot.send_message(message.chat.id, "Переменные являются коэффициентами в соответствующих функциях спроса и предложения: Qd = A*P - B. Qs =C - D*P. Введите коэффициент A:", reply_markup=back_keyboard)
    bot.register_next_step_handler(message, get_coefficient_A_market_equilibrium)

def get_coefficient_A_market_equilibrium(message):
    """
    Получение коэффициента A для нахождения точки рыночного равновесия.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_A = float(message.text)
            
            
            if coefficient_A < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_A_market_equilibrium)
                return

            bot.send_message(message.chat.id, "Введите коэффициент B:")
            bot.register_next_step_handler(message, get_coefficient_B_market_equilibrium, coefficient_A)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_A_market_equilibrium)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_A_market_equilibrium)

def get_coefficient_B_market_equilibrium(message, coefficient_A):
    """
    Получение коэффициента B для нахождения точки рыночного равновесия.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_B = float(message.text)

            
            if coefficient_B < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_B_market_equilibrium, coefficient_A)
                return

            bot.send_message(message.chat.id, "Введите коэффициент C:")
            bot.register_next_step_handler(message, get_coefficient_C_market_equilibrium, coefficient_A, coefficient_B)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_B_market_equilibrium, coefficient_A)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_B_market_equilibrium, coefficient_A)


def get_coefficient_C_market_equilibrium(message, coefficient_A, coefficient_B):
    """
    Получение коэффициента C для нахождения точки рыночного равновесия.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    - coefficient_B (float): Коэффициент B.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_C = float(message.text)

            
            if coefficient_C < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_C_market_equilibrium, coefficient_A, coefficient_B)
                return
            bot.send_message(message.chat.id, "Введите коэффициент D:")
            bot.register_next_step_handler(message, get_coefficient_D_market_equilibrium, coefficient_A, coefficient_B, coefficient_C)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_C_market_equilibrium, coefficient_A, coefficient_B)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_C_market_equilibrium, coefficient_A, coefficient_B)


def calculate_market_equilibrium(A, B, C, D):
    """
    Расчет равновесной цены и объема на рынке.

    Args:
    - A (float): Коэффициент A.
    - B (float): Коэффициент B.
    - C (float): Коэффициент C.
    - D (float): Коэффициент D.

    Returns:
    - Tuple[float, float]: Равновесная цена и объем.
    """

    # Проверка на деление на ноль
    if A + D == 0:
        raise ZeroDivisionError("Деление на ноль невозможно. Знаменатель равен нулю.")
    
    # Рассчитываем равновесную цену (P*) и объем (Q*)
    equilibrium_price = (C + B) / (A + D)
    equilibrium_quantity = A * equilibrium_price - B

    return equilibrium_price, equilibrium_quantity

def get_coefficient_D_market_equilibrium(message, coefficient_A, coefficient_B, coefficient_C):
    """
    Получение коэффициента D для нахождения точки рыночного равновесия.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    - coefficient_B (float): Коэффициент B.
    - coefficient_C (float): Коэффициент C.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_D = float(message.text)

            
            if coefficient_D < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_D_market_equilibrium, coefficient_A, coefficient_B, coefficient_C)
                return

            try:
                # Рассчитываем равновесную цену (P*) и объем (Q*)
                equilibrium_price, equilibrium_quantity = calculate_market_equilibrium(coefficient_A, coefficient_B, coefficient_C, coefficient_D)

                # Отправляем ответ
                response = f"Рыночное равновесие:\nЦена (P*): {equilibrium_price}\nОбъем (Q*): {equilibrium_quantity}"
                bot.send_message(message.chat.id, response)

            except ZeroDivisionError as e:
                # Обработка ошибки деления на ноль
                bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
                handle_back_button(message)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_D_market_equilibrium, coefficient_A, coefficient_B, coefficient_C)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_D_market_equilibrium, coefficient_A, coefficient_B, coefficient_C)


# Обработчик нажатия на кнопку "Расчет объема дефицита/излишка"
@bot.message_handler(func=lambda message: message.text == "Расчет объема дефицита/излишка", content_types=['text'])
def handle_deficit_or_surplus_calculation_start(message):
    """
    Обработчик нажатия на кнопку "Расчет объема дефицита/излишка".

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    # Создаем объект ReplyKeyboardRemove
    remove_keyboard = types.ReplyKeyboardRemove()

    # Создаем клавиатуру с кнопкой "Назад"
    back_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    back_keyboard.add(back_button)

    bot.send_message(message.chat.id, "Переменные являются коэффициентами в соответствующих функциях спроса и предложения: Qd = A*P - B. Qs = C - D*P.", reply_markup=back_keyboard)
    bot.send_message(message.chat.id, "Введите коэффициент A:")
    bot.register_next_step_handler(message, get_coefficient_A_deficit_surplus)

def get_coefficient_A_deficit_surplus(message):
    """
    Получение коэффициента A для расчета объема дефицита/излишка.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_A = float(message.text)

            # Проверка на отрицательное значение
            if coefficient_A < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_A_deficit_surplus)
                return

            bot.send_message(message.chat.id, "Введите коэффициент B:")
            bot.register_next_step_handler(message, get_coefficient_B_deficit_surplus, coefficient_A)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_A_deficit_surplus)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_A_deficit_surplus)

def get_coefficient_B_deficit_surplus(message, coefficient_A):
    """
    Получение коэффициента B для расчета объема дефицита/излишка.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_B = float(message.text)

            # Проверка на отрицательное значение
            if coefficient_B < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_B_deficit_surplus, coefficient_A)
                return

            bot.send_message(message.chat.id, "Введите коэффициент C:")
            bot.register_next_step_handler(message, get_coefficient_C_deficit_surplus, coefficient_A, coefficient_B)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_B_deficit_surplus, coefficient_A)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_B_deficit_surplus, coefficient_A)

def get_coefficient_C_deficit_surplus(message, coefficient_A, coefficient_B):
    """
    Получение коэффициента C для расчета объема дефицита/излишка.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    - coefficient_B (float): Коэффициент B.
"""
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_C = float(message.text)

            # Проверка на отрицательное значение
            if coefficient_C < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_C_deficit_surplus, coefficient_A, coefficient_B)
                return

            bot.send_message(message.chat.id, "Введите коэффициент D:")
            bot.register_next_step_handler(message, get_coefficient_D_deficit_surplus, coefficient_A, coefficient_B, coefficient_C)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_C_deficit_surplus, coefficient_A, coefficient_B)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_C_deficit_surplus, coefficient_A, coefficient_B)

def get_coefficient_D_deficit_surplus(message, coefficient_A, coefficient_B, coefficient_C):
    """
    Получение коэффициента D для расчета объема дефицита/излишка.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    - coefficient_B (float): Коэффициент B.
    - coefficient_C (float): Коэффициент C.
"""
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            coefficient_D = float(message.text)

            # Проверка на отрицательное значение
            if coefficient_D < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение.")
                bot.register_next_step_handler(message, get_coefficient_D_deficit_surplus, coefficient_A, coefficient_B, coefficient_C)
                return

            bot.send_message(message.chat.id, "Введите уровень цены (E):")
            bot.register_next_step_handler(message, get_price_level_deficit_surplus, coefficient_A, coefficient_B, coefficient_C, coefficient_D)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_coefficient_D_deficit_surplus, coefficient_A, coefficient_B, coefficient_C)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_coefficient_D_deficit_surplus, coefficient_A, coefficient_B, coefficient_C)

def get_price_level_deficit_surplus(message, coefficient_A, coefficient_B, coefficient_C, coefficient_D):
    """
    Получение уровня цены для расчета объема дефицита/излишка.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - coefficient_A (float): Коэффициент A.
    - coefficient_B (float): Коэффициент B.
    - coefficient_C (float): Коэффициент C.
    - coefficient_D (float): Коэффициент D.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            price_level = float(message.text)

            # Проверка на отрицательное значение
            if price_level < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для уровня цены (E).")
                bot.register_next_step_handler(message, get_price_level_deficit_surplus, coefficient_A, coefficient_B, coefficient_C, coefficient_D)
                return

            # Рассчитываем спрос и предложение
            demand = coefficient_A * price_level - coefficient_B
            supply = coefficient_C - coefficient_D * price_level

            # Рассчитываем объем дефицита/излишка
            deficit_or_surplus = demand - supply

            # Определяем ситуацию на рынке
            if deficit_or_surplus > 0:
                situation = "дефицита"
            elif deficit_or_surplus < 0:
                situation = "излишка"
            else:
                situation = "равновесия"

            # Отправляем ответ
            response = f"При уровне цены в {price_level} денежных единицах на рынке будет ситуация {situation}. Размер дефицита/излишка составит: {abs(deficit_or_surplus)} единиц товара (при ситуации дефицита/излишка)"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_price_level_deficit_surplus, coefficient_A, coefficient_B, coefficient_C, coefficient_D)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_price_level_deficit_surplus, coefficient_A, coefficient_B, coefficient_C, coefficient_D)

# Словарь для хранения издержек
costs = {
    'variable': [],
    'fixed': []
}

# Максимальное количество издержек
MAX_COSTS = 5

# Обработчик нажатия на кнопку "Расчет прибыли фирмы"
@bot.message_handler(func=lambda message: message.text == "Расчет прибыли фирмы", content_types=['text'])
def handle_profit_calculation_start(message):
    """
    Обработчик нажатия на кнопку "Расчет прибыли фирмы".

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    if message is not None:
        # Создаем объект ReplyKeyboardRemove
        remove_keyboard = types.ReplyKeyboardRemove()



        # Создаем клавиатуру с кнопкой "Назад"
        back_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back_button = types.KeyboardButton('Назад')
        back_keyboard.add(back_button)

        if message.text =='Назад':
            handle_back_button(message) 
            return
        bot.send_message(message.chat.id, "Для расчета прибыли фирмы введите следующие данные:",reply_markup=back_keyboard)
        bot.send_message(message.chat.id, "1. Объем производства в штуках (Q):")
        bot.register_next_step_handler(message, get_firm_production_volume)

def get_firm_production_volume(message):
    """
    Получение объема производства для расчета прибыли фирмы.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    try:
        if message is not None and message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message) 
                return

            Q = float(message.text)

            # Проверка на отрицательное значение
            if Q < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для объема производства.")
                bot.register_next_step_handler(message, get_firm_production_volume)
                return

            bot.send_message(message.chat.id, "2. Цена за единицу товара (P) в рублях:")
            bot.register_next_step_handler(message, get_unit_price, Q)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_firm_production_volume)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Введите числовое значение для объема производства.")
        bot.register_next_step_handler(message, get_firm_production_volume)


def get_unit_price(message, Q):
    """
    Получение цены за единицу товара для расчета прибыли фирмы.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - Q (float): Объем производства.
    """
    try:
        if message.text is not None:
            if message.text =='Назад':
                handle_back_button(message) 
                return
            P = float(message.text)

            # Проверка на отрицательное значение
            if P < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для цены за единицу товара.")
                bot.register_next_step_handler(message, get_unit_price, Q)
                return

            bot.send_message(message.chat.id, f"3. Постоянные издержки (FC) в рублях. Пожалуйста, введите данные в формате 'Название издержки, размер издержки'. (введите 'готово' для завершения, максимум {MAX_COSTS} издержек):")
            bot.register_next_step_handler(message, get_fixed_costs, Q, P)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_unit_price)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Введите числовое значение для цены за единицу товара.")
        bot.register_next_step_handler(message, get_unit_price, Q)

def get_fixed_costs(message, Q, P):
    """
    Получение постоянных издержек для расчета прибыли фирмы.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - Q (float): Объем производства.
    - P (float): Цена за единицу товара.
    """
    if message.text is not None:
        if message.text =='Назад':
            handle_back_button(message) 
            return
        if message.text.lower() == 'готово':
            bot.send_message(message.chat.id, f"4. Переменные издержки (VC) в рублях. Пожалуйста, введите данные в формате 'Название издержки, размер издержки'.  (введите 'готово' для завершения, максимум {MAX_COSTS} издержек):")
            bot.register_next_step_handler(message, get_variable_costs, Q, P)
        else:
            handle_costs_input(message, Q, P, 'fixed')
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_fixed_costs)

def get_variable_costs(message, Q, P):
    """
    Получение переменных издержек для расчета прибыли фирмы.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - Q (float): Объем производства.
    - P (float): Цена за единицу товара.
    """
    if message.text is not None:
        if message.text =='Назад':
            handle_back_button(message) 
            return
        if message.text.lower() == 'готово':
            calculate_and_send_response(message, Q, P)
        else:
            handle_costs_input(message, Q, P, 'variable')
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_variable_costs)

def handle_costs_input(message, Q, P, cost_type):
    """
    Обработка ввода издержек для расчета прибыли фирмы.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - Q (float): Объем производства.
    - P (float): Цена за единицу товара.
    - cost_type (str): Тип издержек ('fixed' или 'variable').
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return

            input_costs = message.text.split(', ')
            name, cost = input_costs[0], float(input_costs[1])

            # Проверка на неотрицательное значение
            if cost < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для издержек.")
                bot.register_next_step_handler(message, handle_costs_input, Q, P, cost_type)
                return

            if len(costs[cost_type]) < MAX_COSTS:
                costs[cost_type].append((name, cost))
                bot.send_message(message.chat.id, f"Добавлены {cost_type} издержки: {name}, {cost}. Введите следующие или 'Готово'.")
                bot.register_next_step_handler(message, get_fixed_costs, Q, P) if cost_type == 'fixed' else bot.register_next_step_handler(message, get_variable_costs, Q, P)
            else:
                bot.send_message(message.chat.id, f"Достигнуто максимальное количество {cost_type} издержек ({MAX_COSTS}). Введите 'Готово'.")
                bot.register_next_step_handler(message, get_fixed_costs, Q, P) if cost_type == 'fixed' else bot.register_next_step_handler(message, get_variable_costs, Q, P)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, handle_costs_input)
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Некорректный ввод. Пожалуйста, введите данные в формате 'Название издержки, размер издержки'.")
        bot.register_next_step_handler(message, get_fixed_costs, Q, P) if cost_type == 'fixed' else bot.register_next_step_handler(message, get_variable_costs, Q, P)

def calculate_and_send_response(message, Q, P):
    """
    Рассчитывает прибыль фирмы и отправляет ответ пользователю.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - Q (float): Объем производства.
    - P (float): Цена за единицу товара.
    """
    try:
        # Суммируем постоянные издержки
        total_fixed_costs = sum(item[1] for item in costs['fixed'])

        # Суммируем переменные издержки
        total_variable_costs = sum(item[1] for item in costs['variable'])

        # Источники постоянных издержек
        fixed_costs_sources = ', '.join([f'{source[0]}, {source[1]} руб.' for source in costs['fixed']])

        # Источники переменных издержек
        variable_costs_sources = ', '.join([f'{source[0]} ({source[1]} руб./единицу товара)' for source in costs['variable']])

        # Рассчитываем прибыль
        profit = Q * (P - total_variable_costs) - total_fixed_costs

        response = (
            f"При реализации {Q} единиц продукции по {P} руб. за единицу товара и уровне "
            f"переменных издержек в {total_variable_costs} руб./единицу товара "
            f"(включая: {variable_costs_sources}), "
            f"и постоянных издержек в {total_fixed_costs} руб. "
            f"(включая: {fixed_costs_sources}), прибыль составит: {profit} руб."
        )

        bot.send_message(message.chat.id, response)
        
        costs['variable'].clear()
        costs['fixed'].clear()

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при расчете прибыли. Пожалуйста, проверьте введенные данные.")
        print(e)

# Обработчик нажатия на кнопку "Назад"
@bot.message_handler(func=lambda message: message.text.lower() == 'назад')
def handle_back_button(message):
    """
    Обработчик нажатия на кнопку "Назад". Возвращает пользователя на главный экран.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    # Создаем клавиатуру с задачами
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton("Построение общей КПВ")
    button2 = types.KeyboardButton("Нахождение точки рыночного равновесия")
    button3 = types.KeyboardButton("Расчет объема дефицита/излишка")
    button4 = types.KeyboardButton("Расчет прибыли фирмы")
    
    keyboard.add(button1, button2, button3, button4)
    
    # Отправляем клавиатуру с сообщением
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Построение общей КПВ"
@bot.message_handler(func=lambda message: message.text == "Построение общей КПВ")
def handle_build_kpv(message):
    """
    Обработчик нажатия на кнопку "Построение общей КПВ". Инициирует процесс ввода данных для
    построения кривой предложения.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    remove_keyboard = types.ReplyKeyboardRemove()

    # Клавиатура с кнопкой "Назад"
    back_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    back_keyboard.add(back_button)

    bot.send_message(message.chat.id, "Введите максимальный объем производства товара А для производителя 1:", reply_markup=back_keyboard)
    bot.register_next_step_handler(message, get_max_production_A1)

def get_max_production_A1(message):
    """
    Обработчик ввода максимального объема производства товара А для производителя 1.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    """
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return
            max_production_A1 = float(message.text)
            while max_production_A1 < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для максимального объема производства товара А для производителя 1:")
                bot.register_next_step_handler(message, get_max_production_A1)
                return

            bot.send_message(message.chat.id, "Введите максимальный объем производства товара Б для производителя 1:")
            bot.register_next_step_handler(message, get_max_production_B1, max_production_A1)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_max_production_A1)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_max_production_A1)

def get_max_production_B1(message, max_production_A1):
    """
    Обработчик ввода максимального объема производства товара Б для производителя 1.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - max_production_A1 (float): Максимальный объем производства товара А для производителя 1.

"""
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return
            max_production_B1 = float(message.text)
            while max_production_B1 < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для максимального объема производства товара Б для производителя 1:")
                bot.register_next_step_handler(message, get_max_production_B1, max_production_A1)
                return

            bot.send_message(message.chat.id, "Введите максимальный объем производства товара А для производителя 2:")
            bot.register_next_step_handler(message, get_max_production_A2, max_production_A1, max_production_B1)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_max_production_B1, max_production_A1)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_max_production_B1, max_production_A1)

def get_max_production_A2(message, max_production_A1, max_production_B1):
    """
    Обработчик ввода максимального объема производства товара А для производителя 2.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - max_production_A1 (float): Максимальный объем производства товара А для производителя 1.
    - max_production_B1 (float): Максимальный объем производства товара Б для производителя 1.
"""
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return
            max_production_A2 = float(message.text)
            while max_production_A2 < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для максимального объема производства товара А для производителя 2:")
                bot.register_next_step_handler(message, get_max_production_A2, max_production_A1, max_production_B1)
                return

            bot.send_message(message.chat.id, "Введите максимальный объем производства товара Б для производителя 2:")
            bot.register_next_step_handler(message, get_max_production_B2, max_production_A1, max_production_B1, max_production_A2)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_max_production_A2, max_production_A1, max_production_B1)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_max_production_A2, max_production_A1, max_production_B1)

def get_max_production_B2(message, max_production_A1, max_production_B1, max_production_A2):
    """
    Обработчик ввода максимального объема производства товара Б для производителя 2.

    Args:
    - message (types.Message): Объект сообщения пользователя.
    - max_production_A1 (float): Максимальный объем производства товара А для производителя 1.
    - max_production_B1 (float): Максимальный объем производства товара Б для производителя 1.
    - max_production_A2 (float): Максимальный объем производства товара А для производителя 2.
"""
    try:
        if message.text is not None:
            if message.text == 'Назад':
                handle_back_button(message)
                return
            max_production_B2 = float(message.text)
            while max_production_B2 < 0:
                bot.send_message(message.chat.id, "Пожалуйста, введите неотрицательное числовое значение для максимального объема производства товара Б для производителя 2:")
                bot.register_next_step_handler(message, get_max_production_B2, max_production_A1, max_production_B1, max_production_A2)
                return

            # Построение графика общей КПВ
            plot_kpv(max_production_A1, max_production_B1, max_production_A2, max_production_B2)

            bot.send_photo(message.chat.id, open('kpv_plot.png', 'rb'))
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
            bot.register_next_step_handler(message, get_max_production_B2, max_production_A1, max_production_B1, max_production_A2)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите числовое значение.")
        bot.register_next_step_handler(message, get_max_production_B2, max_production_A1, max_production_B1, max_production_A2)

def plot_kpv(max_production_A_1, max_production_B_1, max_production_A_2, max_production_B_2):
    """
    Строит график кривой производственных возможностей для двух производителей с использованием точек A, B и C.

    Parameters:
    - max_production_A_1 (float): Максимальный объем производства товара A для производителя 1.
    - max_production_B_1 (float): Максимальный объем производства товара B для производителя 1.
    - max_production_A_2 (float): Максимальный объем производства товара A для производителя 2.
    - max_production_B_2 (float): Максимальный объем производства товара B для производителя 2.

    Генерирует график кривой производственных возможностей и сохраняет его в файл 'kpv_plot.png'.
    """

    # Создаем списки значений для точек a, b и c
    point_a = [max_production_A_1 + max_production_A_2, 0]
    point_b = [max(max_production_A_1, max_production_A_2), max(max_production_B_1, max_production_B_2)]
    point_c = [0, max_production_B_1 + max_production_B_2]

    # Извлечение координат точек
    a_x, a_y = point_a
    b_x, b_y = point_b
    c_x, c_y = point_c

    # Построение графика с точками
    plt.figure(figsize=(8, 6))
    plt.scatter([a_x, b_x, c_x], [a_y, b_y, c_y], color='red', label='Точки')

    # Проводим отрезки через точки
    plt.plot([b_x, c_x], [b_y, c_y], color='green', linestyle='--', label='Производитель 1')
    plt.plot([a_x, b_x], [a_y, b_y], color='blue', linestyle='--', label='Производитель 2')
    

    # Добавление названий точек
    plt.text(a_x, a_y, 'C', fontsize=12, ha='right', va='bottom')
    plt.text(b_x, b_y, 'B', fontsize=12, ha='left', va='top')
    plt.text(c_x, c_y, 'A', fontsize=12, ha='right', va='top')

    # Настройки графика
    plt.title('Общая КПВ')
    plt.xlabel('Производство товара Б')
    plt.ylabel('Производство товара A')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('kpv_plot.png')
    plt.close()


# Запускаем бота
bot.polling(none_stop=True)
