'''All the functions thats handle the cart'''

from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from loader import bot
from data import carrito
from constants import EMPTY_CART, CHECKOUT, CHANGE_QUANTITY, DELETE_PRODUCT


def show_cart(chat_id):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    inline_markup.row(InlineKeyboardButton(
        CHECKOUT, callback_data="Finalizar Compra"))
    inline_markup.add(
        InlineKeyboardButton(
            DELETE_PRODUCT, callback_data="eliminar producto"),
        InlineKeyboardButton(
            CHANGE_QUANTITY, callback_data="cantidad"),
        InlineKeyboardButton(
            EMPTY_CART, callback_data="Vaciar Carrito")
    )

    if (chat_id not in carrito or not carrito):
        bot.send_message(
            chat_id, "😅 <b>Tu carrito está vacío.</b> \n\n¡Escoge algún producto!")
    else:
        mensaje = calculate_products_in_cart(chat_id)
        bot.send_message(chat_id, mensaje, reply_markup=inline_markup)


# Calculate the quantity of products in the cart and return the text'
def calculate_products_in_cart(chat_id):
    total = 0
    mensaje = "<b>Productos en el carrito:</b>\n\n"

    for nombre, producto in carrito[chat_id].items():
        subtotal = producto["precio"] * producto["cantidad"]
        total += subtotal
        mensaje += f"- <i>{nombre}</i> ({producto['cantidad']} x ${producto['precio']} = ${subtotal})\n\n"

    mensaje += f"<b>💰 TOTAL:</b> ${total} MN"
    return mensaje
