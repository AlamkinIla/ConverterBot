import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    help_text = """
💵 *Конвертер валют ЦБ РФ* 💵

Отправьте запрос в формате:
*<валюта1> <валюта2> <количество>*

Примеры:
• USD RUB 100 - переведет 100 долларов в рубли
• EUR USD 50 - переведет 50 евро в доллары
• RUB EUR 5000 - переведет 5000 рублей в евро

Доступные валюты: USD, EUR, RUB
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['values'])
def send_values(message):
    values_text = """
📊 *Поддерживаемые валюты:*
- USD (доллар США)
- EUR (евро)
- RUB (российский рубль)
"""
    bot.send_message(message.chat.id, values_text, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Удаляем ВСЕ слеши (если есть) и лишние пробелы
        text = message.text.replace('/', '').strip()
        parts = text.split()

        if len(parts) != 3:
            raise APIException("❌ Нужно 3 параметра: <валюта1> <валюта2> <количество>\nПример: USD RUB 500")

        base, quote, amount = parts
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(
            message.chat.id,
            f"💱 *{amount} {base.upper()} = {result:.2f} {quote.upper()}*",
            parse_mode="Markdown"
        )

    except APIException as e:
        bot.send_message(message.chat.id, str(e), parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {str(e)}", parse_mode="Markdown")


if __name__ == '__main__':
    print("Бот запущен и готов к работе! 🚀")
    bot.polling(none_stop=True)