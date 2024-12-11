from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Глобальные переменные для хранения данных
duty_schedule = ["Алиса", "Борис", "Виктор", "Галина"]
user_schedules = {}  # Словарь для хранения расписаний пользователей

# Функция для отображения текущего дежурного
async def show_duty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    week_number = 0  # Номер недели, можно сделать динамическим
    current_duty = duty_schedule[week_number % len(duty_schedule)]
    await update.message.reply_text(f'Сегодня дежурный: {current_duty}')

# Функция для установки списка дежурных
async def set_duties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global duty_schedule
    duty_schedule = context.args
    await update.message.reply_text(f'Обновлён список дежурных: {", ".join(duty_schedule)}')

# Функция для отображения расписания пользователя
async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = ' '.join(context.args).strip()
    if user in user_schedules:
        schedule = user_schedules[user]
        await update.message.reply_text(f'Расписание {user}: {schedule}')
    else:
        await update.message.reply_text(f'Расписание для {user} не найдено.')

# Функция для изменения расписания пользователя
async def set_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Используйте: /set_schedule [Имя] [Расписание]")
        return
    user = args[0]
    schedule = ' '.join(args[1:])
    user_schedules[user] = schedule
    await update.message.reply_text(f'Расписание для {user} обновлено: {schedule}')

# Основная функция
async def main():
    # Подставьте ваш реальный токен здесь
    app = ApplicationBuilder().token("7502031975:AAGhSpo_ip_xggTfW8eiWDgBshJJnXI6nYY").build()

    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("duty", show_duty))
    app.add_handler(CommandHandler("set_duties", set_duties))
    app.add_handler(CommandHandler("schedule", show_schedule))
    app.add_handler(CommandHandler("set_schedule", set_schedule))

    # Запуск бота
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())