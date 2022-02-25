import telebot

class TelegramService:

    def __init__(self, api_key, chat_id):
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(api_key)

    def send_msg(self, msg):
        self.bot.send_message(self.chat_id, msg)