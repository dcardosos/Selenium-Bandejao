import telebot
from dotenv import load_dotenv
import os
from scrapping import Scrapping

load_dotenv()

CHAVE_API = os.getenv('CHAVE_API_BANDEIJAO_BOT')
bot = telebot.TeleBot(CHAVE_API)


@bot.message_handler(commands=['central'])
def central(mensagem):
    obj = Scrapping("central")
    bot.send_message(mensagem.chat.id, obj.cardapio_now())

@bot.message_handler(commands=['fisica'])
def fisica(mensagem):
    obj = Scrapping("fisica")
    bot.send_message(mensagem.chat.id, obj.cardapio_now())

@bot.message_handler(command=['quimica'])
def quimica(mensagem):
    obj = Scrapping("quimica")
    bot.send_message(mensagem.chat.id, obj.cardapio_now())

def verificar(message):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
Escolha um bandeijão (clique na opção):
    /central Bandeijao central
    /fisica Bandeijao da fisica
    /quimica Bandeijao da quimica
    """
    bot.send_message(mensagem.chat.id, texto)
bot.polling() # looping

