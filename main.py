'''The main file'''
import telebot
import random
# para crear un tunel entre el servidor web local y una URL pública en internet
# from pyngrok import ngrok, conf
from waitress import serve
from telebot import time
from loader import bot, web_server
from constants import WELCOME_TEXT, ABOUT_SHOP, STICKER_NINJA_WELCOME_GREAT, NGROK_TOKEN
from modules.keyboards import categories_buttons, keyboards_buttons


@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''Maneja el comando /start'''
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, " 🇯🇵 <b>¡BIENVENIDO!</b> 🇯🇵")
    time.sleep(2)
    bot.edit_message_text("🇯🇵 <b>¡IRASSHAIMASE!</b> 🇯🇵",
                          chat_id, msg.message_id)
    msg = bot.send_sticker(chat_id, STICKER_NINJA_WELCOME_GREAT)
    time.sleep(6)
    bot.delete_message(chat_id, msg.message_id)
    bot.send_message(chat_id, WELCOME_TEXT)
    keyboards_buttons(message)
    categories_buttons(chat_id)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, ABOUT_SHOP)


# Manejador para el evento de mensaje
@bot.message_handler(content_types=["text", "photo", "audio", "document", "" "sticker", "video", "contact", "location"])
def on_message(message):
    # Obtén el ID del chat y el texto del mensaje
    chat_id = message.chat.id

    # Lista de IDs de los packs de stickers
    pack_ids = ['ShinobiAssassin',
                'Gojiil_Emoji_248', 'GojillS1ick3r', 'Gojill2S1ick3r']

    # Selecciona un ID de pack de manera aleatoria
    random_pack_id = random.choice(pack_ids)

    # Obtiene la información del pack de stickers
    pack = bot.get_sticker_set(random_pack_id)

    # Selecciona un sticker aleatorio del pack
    random_sticker = random.choice(pack.stickers)

    # Envía el sticker al chat
    msg = bot.send_sticker(chat_id, random_sticker.file_id)
    time.sleep(6)
    bot.delete_message(chat_id, message.message_id)
    bot.delete_message(chat_id, msg.message_id)


# configurar menu comandos
bot.set_my_commands([telebot.types.BotCommand("/start", "Te damos la bienvenida"),
                    telebot.types.BotCommand("/help", "¿Cómo puedo comprar?")])

# Ejecuta el bot
# definimos la ruta del arhivo de configuracion de ngrok
# conf.get_default().config_path = "./config_ngrok.yml"
# configuramos la región del servidor de ngrok
# conf.get_default().region = "us"
# crear el archivo de credenciales de la API de ngrok
# ngrok.set_auth_token(NGROK_TOKEN)
# crear un túnel HTTPS en el puerto 5000
# ngrok_tunel = ngrok.connect(5000, bind_tls=True)
# URL del túnel creado
# ngrok_url = ngrok_tunel.public_url
# print("URL NGROK: ", ngrok_url)
# eliminar webhook anterior
if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(1)
    # definir el webhook
    bot.set_webhook(url="https://infinitetreasuresbot.up.railway.app/")
    # iniciar el servidor
    serve(web_server, host="0.0.0.0", port=443)
    # web_server.run(host="0.0.0.0", port=5000)

    # bot.infinity_polling(timeout=30, skip_pending=True)
