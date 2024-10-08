import datetime
import os

import telebot
import yfinance as yf

API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["stocks"])
def get_stocks(message):
    today = datetime.datetime.now().strftime("%B %d, %A")
    response = ""
    stocks = ["VOO", "F", "AAPL"]
    stock_data = []
    columns = ["Stock", "Price", "%Change"]

    for stock in stocks:
        data = yf.download(stock, period="1d", interval="1d")
        data = data.reset_index()
        stock_info = [stock]

        for index, row in data.iterrows():
            open_price = row["Open"]
            close_price = row["Close"]
            current_price = round(close_price, 2)
            change = round((((close_price - open_price) / open_price) * 100), 2)
            stock_info.append(current_price)
            if change >= 0:
                stock_info.append(f"+{change}%")
            else:
                stock_info.append(f"{change}%")

        stock_data.append(stock_info)

        response = f"{today}\n"
        response += "```\n"
        response += f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
        response += "-" * 30 + "\n"
        for row in stock_data:
            response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
        response += "```"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


bot.polling()
