'''This modules have the handlers of the bot'''

import urllib.parse
from telebot import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from modules.cart import show_cart, calculate_products_in_cart
from data import user_shop, productos, carrito, get_user_state, set_user_state
from constants import *
from loader import bot


def categories_buttons(chat_id):
    '''Categories Buttons'''
    inline_markup = InlineKeyboardMarkup(row_width=2)
    inline_markup.add(
        InlineKeyboardButton(KEYS, callback_data="Llavero"),
        InlineKeyboardButton(AGENDAS, callback_data="Agenda"))
    inline_markup.row(InlineKeyboardButton(
        PAPERCRAFTS, callback_data="Papercraft"))
    inline_markup.add(
        InlineKeyboardButton(STICKERS, callback_data="Calcomanía"),
        InlineKeyboardButton(POSTERS, callback_data="Poster"),
        InlineKeyboardButton(ABOUT_US, callback_data="about"))
    bot.send_message(
        chat_id, "Por favor, escoge una categoría:", reply_markup=inline_markup)


def keyboards_buttons(message):
    '''Keyboard buttons'''
    keyboard_markup = ReplyKeyboardMarkup(
        input_field_placeholder="Escoge una categoría:", resize_keyboard=True)
    keyboard_markup.add(CATEGORIES, CART)
    bot.send_message(message.chat.id, "⛩⛩⛩", reply_markup=keyboard_markup)


@bot.message_handler(func=lambda message: message.text in [CATEGORIES, CART])
def handle_keyboard(message):
    '''Manejador para la respuesta del teclado personalizado'''
    chat_id = message.chat.id
    if message.text == CATEGORIES:
        categories_buttons(chat_id)
    elif message.text == CART:
        show_cart(chat_id)


#         DECORADORES       #


# Decorador para verificar si el usuario está en estado "esperando"
def check_user_waiting_state(func):
    def wrapper(call):
        chat_id = call.from_user.id
        if get_user_state(chat_id) == "waiting":
            bot.answer_callback_query(
                call.id, "¡Lo siento, estoy esperando tu respuesta!")
        else:
            func(call)
    return wrapper


# Decorador para agregar un tipo de producto
@check_user_waiting_state
def add_product_type_handler(call):
    chat_id = call.from_user.id
    product_type = call.data
    add_product_type(chat_id, product_type)


# Decorador para mostrar el producto Action's Figures
@check_user_waiting_state
def show_action_figure_handler(call):
    chat_id = call.from_user.id
    photo = open(productos["Figuras de acción"]["imagen"], "rb")
    text = productos["Figuras de acción"]["texto"]
    bot.send_photo(chat_id, photo, text)


# Decorador para mostrar el carrito
@ check_user_waiting_state
def show_cart_handler(call):
    chat_id = call.from_user.id
    show_cart(chat_id)


# Decorador para escoger un producto y cambiar su cantidad
@ check_user_waiting_state
def show_products_to_change_quantity_handler(call):
    chat_id = call.from_user.id
    show_products_in_cart_to_change(chat_id)


# Decorador para cambiar la cantidad del producto escogido
@ bot.callback_query_handler(func=lambda call: call.data.startswith('change'))
@ check_user_waiting_state
def change_quantity_handler(call):
    chat_id = call.from_user.id
    producto = call.data.split()[1]
    if chat_id not in carrito or producto not in carrito[chat_id]:
        bot.send_message(chat_id, "😅 Ese producto no está en tu carrito")
    else:
        set_user_state(chat_id, "waiting")
        msg = bot.send_message(
            chat_id, "Escribe la cantidad:", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(
            msg, change_amount, producto)


# Decorador para escoger un producto y eliminarlo del carrito
@check_user_waiting_state
def show_products_to_delete_handler(call):
    chat_id = call.from_user.id
    show_products_in_cart_to_delete(chat_id)


# Decorador para eliminar el producto escogido
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete'))
@check_user_waiting_state
def delete_product_from_cart_handler(call):
    chat_id = call.from_user.id
    producto = call.data.split()[1]
    if chat_id not in carrito or producto not in carrito[chat_id]:
        bot.send_message(chat_id, "😅 Ese producto no está en tu carrito")
    elif len(carrito[chat_id]) == 1:
        empty_cart(chat_id)
    else:
        del carrito[chat_id][producto]
        bot.send_message(
            chat_id, f"<b>{producto}</b> ha sido eliminado del carrito")


# Decorador para vaciar el carrito
@check_user_waiting_state
def delete_cart_handler(call):
    chat_id = call.from_user.id
    empty_cart(chat_id)


# Decorador para mostrar las categorías de los productos
@check_user_waiting_state
def categories_handler(call):
    chat_id = call.from_user.id
    categories_buttons(chat_id)


# Decorador para finalizar la compra
@check_user_waiting_state
def checkout_handler(call):
    chat_id = call.from_user.id
    if chat_id not in carrito:
        bot.send_message(
            chat_id, "😅 <b>Tu carrito está vacío.</b> \n\n¡Escoge algún producto!")
    else:
        set_user_state(chat_id, "waiting")
        msg = bot.send_message(
            chat_id, "¡PERSONALIZA TU PEDIDO! \nEscoge tu serie o personaje favorito. \n\n<b>Descríbenos cómo quieres tu producto:</b>", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(
            msg, checkout)


# Decorador para comprar un producto
@check_user_waiting_state
def shopping_handler(call):
    chat_id = call.from_user.id
    shopping(chat_id)
    bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=None)


# Decorador para manejar las acciones de los botones inline del bot
@bot.callback_query_handler(func=lambda call: True)
def inline_buttons_handler(call):
    action = call.data
    handlers = {
        "Llavero": add_product_type_handler,
        "Agenda": add_product_type_handler,
        "Calcomanía": add_product_type_handler,
        "Papercraft": lambda call: inline_buttons_papercraft(call.from_user.id),
        "Chibi": add_product_type_handler,
        "Poster3D": add_product_type_handler,
        "Figuras de acción": add_product_type_handler,
        "Poster": add_product_type_handler,
        "about": lambda call: bot.send_message(call.from_user.id, ABOUT_SHOP),
        "Carrito": show_cart_handler,
        "cantidad": show_products_to_change_quantity_handler,
        f"change f{{call.data.split()[1]}}": change_quantity_handler,
        "eliminar producto": show_products_to_delete_handler,
        f"delete f{{call.data.split()[1]}}": delete_product_from_cart_handler,
        "Vaciar Carrito": delete_cart_handler,
        "categories": categories_handler,
        "comprar": shopping_handler,
        "Finalizar Compra": checkout_handler
    }
    handlers.get(action, lambda call: None)(call)


#         UTILITY FUNCTIONS       #


def add_product_type(chat_id, type_product):
    '''Handle add product's type'''
    if chat_id in user_shop:
        del user_shop[chat_id]
    user_shop[chat_id] = {}
    user_shop[chat_id][type_product] = {
        "precio": productos[type_product]["precio"], "cantidad": 1, "stock": productos[type_product]["stock"]}
    product_message(
        chat_id, productos[type_product]["imagen"], productos[type_product]["texto"], type_product)


def product_message(chat_id, photo, text, producto):
    '''Handle_product_message'''
    foto = open(photo, "rb")
    # ShopNow Button
    if user_shop[chat_id][producto]["stock"] == "AGOTADO":
        bot.send_photo(chat_id, foto, text)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        shop = InlineKeyboardButton(SHOP_NOW, callback_data="comprar")
        markup.add(shop)
        bot.send_photo(chat_id, foto,
                       text, reply_markup=markup)


def inline_buttons_papercraft(chat_id):
    '''Papercrafts inline buttons'''
    inline_markup = InlineKeyboardMarkup(row_width=3)
    inline_markup.add(
        InlineKeyboardButton(CHIBI, callback_data="Chibi"),
        InlineKeyboardButton(POSTER3D, callback_data="Poster3D"),
        InlineKeyboardButton(ACTION_FIGURES, callback_data="Figuras de acción"))
    bot.send_message(
        chat_id, "Tipos de papercraft:", reply_markup=inline_markup)


def shopping(chat_id):
    if chat_id not in carrito:
        carrito[chat_id] = user_shop[chat_id]
    else:
        for producto in user_shop[chat_id]:
            if producto in carrito[chat_id]:
                carrito[chat_id][producto]["cantidad"] += 1
            else:
                carrito[chat_id][producto] = user_shop[chat_id][producto]
    shopping_inline_buttons(chat_id)


def shopping_inline_buttons(chat_id):
    ''' Product's comments inline buttons'''
    inline_markup = InlineKeyboardMarkup(row_width=1)
    inline_markup.add(
        InlineKeyboardButton(SEE_CART, callback_data="Carrito"),
        InlineKeyboardButton(CHECKOUT, callback_data="Finalizar Compra"),
        InlineKeyboardButton(KEEP_SHOPPING, callback_data="categories"))
    bot.send_message(
        chat_id, "Pedido agregado al carrito.", reply_markup=inline_markup)


def show_products_in_cart_to_change(chat_id):
    '''Choose the product to change'''
    if (chat_id not in carrito or not carrito):
        bot.send_message(
            chat_id, "😅 <b>Tu carrito está vacío.</b> \n\n¡Escoge algún producto!")
    else:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        for name, producto in carrito[chat_id].items():
            inline_markup.add(InlineKeyboardButton(
                f"{name}", callback_data=f"change {name}"))
        bot.send_message(
            chat_id, "Escoge el producto para cambiar la cantidad:", reply_markup=inline_markup)


def show_products_in_cart_to_delete(chat_id):
    '''Choose the product to delete'''
    if (chat_id not in carrito or not carrito):
        bot.send_message(
            chat_id, "😅 <b>Tu carrito está vacío.</b> \n\n¡Escoge algún producto!")
    else:
        inline_markup = InlineKeyboardMarkup(row_width=1)
        for name, producto in carrito[chat_id].items():
            inline_markup.add(InlineKeyboardButton(
                f"{name}", callback_data=f"delete {name}"))
        bot.send_message(
            chat_id, "Escoge el producto que quieres eliminar:", reply_markup=inline_markup)


def change_amount(message, producto):
    '''Change the quantity of the product'''
    try:
        chat_id = message.chat.id
        amount = int(message.text)
        if amount <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        carrito[chat_id][producto]["cantidad"] = amount
        text = f"La cantidad de {producto} se ha actualizado a {amount}"
        bot.send_message(chat_id, text)
        keyboards_buttons(message)
        set_user_state(chat_id, None)
        show_cart(chat_id)
    except ValueError:
        msg = bot.send_message(
            chat_id, " 😵‍💫 <b>Por favor, escribe un número entero mayor que cero.</b>\n\nVuelve a intentarlo")
        bot.register_next_step_handler(
            msg, change_amount, producto)


def empty_cart(chat_id):
    '''Handle cart delete'''
    if chat_id not in carrito:
        bot.send_message(chat_id, "😅 Tu carrito ya está vacío")
    else:
        del carrito[chat_id]
        bot.send_message(
            chat_id, "Tu carrito ha sido vaciado")


def checkout(message):
    '''Handle the client checkout'''
    chat_id = message.chat.id
    pedido = calculate_products_in_cart(chat_id)
    pedido += f'\n\n<b>Personalización del pedido:</b> \n{message.text}'
    # If the user has no username
    if not message.from_user.username:
        bot.send_sticker(
            chat_id, STICKER_NINJA_THINKING)
        time.sleep(3)
        mensaje = '             ⁉️⁉️<b>ALERTA</b>⁉️⁉️\n\n\
             ¡Hola! Veo que no tienes un <b>nombre de usuario</b>. 🤔 Sin un nombre de usuario, el comercio no puede ponerse en contacto contigo. \
            \n\nPor favor, haz clic en este enlace para enviar los datos del pedido:\n\n\
        https://t.me/Aridminos\n\n\
        Copia y pega tu pedido, que te muestro en el <b>próximo</b> mensaje.'
        bot.send_message(chat_id, mensaje)
        time.sleep(1)
        bot.send_message(
            chat_id, "<b><i>Este es tu pedido. Copialo y envíalo:\n\n</i></b>" + pedido)
        del carrito[chat_id]
        set_user_state(chat_id, None)
        bot.send_message(chat_id, "<b>¡Envía tu pedido y será procesado!</b> \n\n  De todos modos, te aconsejamos que te crees un <b>nombre de usuario</b>, para que tus futuras interacciones en esta tienda y en Telegram sean más sencillas\n\n\
                         <b>¡Gracias por tu compra!</b>")
        keyboards_buttons(message)

    # if the user has username
    else:
        bot.send_message(
            CHAT_ID_ARIADNA, f"{message.chat.first_name} {message.chat.last_name} (@{message.chat.username}) ha realizado un pedido: \n\n{pedido}")
        bot.send_sticker(
            chat_id, STICKER_NINJA_ARIGATO)
        time.sleep(2)
        bot.send_message(
            chat_id, "¡¡¡BRAVO!!! \n\n<b>Tu pedido ha sido enviado y está siendo procesado</b>")
        empty_cart(chat_id)
        set_user_state(chat_id, None)
        keyboards_buttons(message)
        categories_buttons(chat_id)


# Send the pedido if the user has no username
def user_has_no_username(chat_id, pedido):
    # perfil = "https://t.me/Aridminos"
    mensaje_pedido = "Hola, quisiera hacer un pedido: " + pedido
    # query = {"url": perfil, "text": mensaje}
    # encoded_query = urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
    encoded_query = urllib.parse.quote(mensaje_pedido)

    link = f"tg://resolve?domain=Aridminos&text=prueba"

    mensaje = 'Hola! Veo que no tienes un nombre de usuario. \n\nPor favor, haz clic en este enlace para enviar los datos del pedido:\n\n' + \
        'https://t.me/Aridminos?start=prueba'

    # mensaje = f'Hola! Veo que no tienes un nombre de usuario. \n\nPor favor, haz clic en este enlace para enviar los datos del pedido:\n\n{link}.'
    bot.send_message(chat_id, mensaje)
