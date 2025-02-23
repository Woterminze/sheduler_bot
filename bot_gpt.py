import telebot
from datetime import datetime, timedelta
import re
from telebot.types import BotCommand

# Токен, полученный у BotFather
TOKEN = "7502031975:AAGhSpo_ip_xggTfW8eiWDgBshJJnXI6nYY"
bot = telebot.TeleBot(TOKEN)

# Список дежурных
duty_list = ["Яна", "Таня", "Булат", "Юля"]
# Словарь с расписанием дежурств и участников (список расписаний для каждого участника)
schedule = {}


# Убираем никнейм бота из команды с помощью регулярного выражения
def clean_command_text(message, command):
    return re.sub(f"/{command}(?:@{bot.get_me().username})?", f"/{command}", message.text).strip()


# Команда для установки дежурных
# @bot.message_handler(commands=["set_duty"])
# def set_duty(message):
#     global duty_list
#     command_text = clean_command_text(message, "set_duty")
#     names = command_text.split()[1:]
#     duty_list = names
#     bot.reply_to(message, "Список дежурных установлен.")
#     if message == "/set_duty@testers_scheduler_bot":
#         bot.reply_to(message, "Введите команду и список дежурных через пробел")

# Команда для показа списка дежурных по порядку
@bot.message_handler(commands=["list_duties"])
def list_duties(message):
    if not duty_list:
        bot.reply_to(message, "Список дежурных не установлен.")
        return
    # Формируем список дежурных
    duties = "\n".join(f"{i + 1}. {name}" for i, name in enumerate(duty_list))
    bot.reply_to(message, f"Список дежурных:\n{duties}")


# Команда для показа текущего дежурного с диапазоном дат
@bot.message_handler(commands=["who_is_on_duty"])
def who_is_on_duty(message):
    if not duty_list:
        bot.reply_to(message, "Список дежурных не установлен.")
        return

    # Определение текущей недели и вычисление дат
    today = datetime.now().date()
    week_num = (today - datetime(today.year, 1, 1).date()).days // 7
    current_duty = duty_list[week_num % len(duty_list)]

    # Начало и конец текущей недели (понедельник - воскресенье)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Форматируем вывод с датами
    bot.reply_to(
        message,
        f"Дежурный на этой неделе: {current_duty}\n"
        f"Период дежурства: {start_of_week.strftime('%d.%m.%Y')} - {end_of_week.strftime('%d.%m.%Y')}"
    )


# # Команда для добавления расписания участнику
# @bot.message_handler(commands=["add_schedule"])
# def add_schedule(message):
#     command_text = clean_command_text(message, "add_schedule")
#     try:
#         args = command_text.split(maxsplit=2)
#         name = args[1]
#         new_schedule = args[2]
#         if name not in schedule:
#             schedule[name] = []
#         schedule[name].append(new_schedule)
#         bot.reply_to(message, f"Новое расписание для {name} добавлено.")
#     except IndexError:
#         bot.reply_to(message, "Используйте команду так: /add_schedule <имя> <расписание>")

# # Команда для просмотра расписания участника на этой неделе
# @bot.message_handler(commands=["show_schedule"])
# def show_schedule(message):
#     command_text = clean_command_text(message, "show_schedule")
#     name = command_text.split(maxsplit=1)[1] if len(command_text.split()) > 1 else ""
#     if name not in schedule or not schedule[name]:
#         bot.reply_to(message, f"У {name} пока нет расписания.")
#         return
#     # Чередуем расписание на основе номера недели
#     today = datetime.now().date()
#     week_num = (today - datetime(today.year, 1, 1).date()).days // 7
#     current_schedule = schedule[name][week_num % len(schedule[name])]
#     bot.reply_to(message, f"Расписание для {name} на эту неделю: {current_schedule}")

# Команда для помощи
@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(message, (
        "/list_duties Показать список дежурных(задается Таней)\n"
        "/who_is_on_duty - Показать, кто дежурный на этой неделе с диапазоном дат\n"
    ))


# Запуск бота
bot.polling()