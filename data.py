'''All the data of the bot'''

from constants import \
    LLAVEROS_TEXT, \
    AGENDAS_TEXT, \
    STICKERS_TEXT, \
    CHIBI_TEXT, \
    POSTER3D_TEXT, \
    ACTION_FIGURES_TEXT, \
    POSTERS_TEXT

# Dictionary for storage the products in the car
carrito = {}

# Temporal Dictionary for storage the state of the user's shop
user_shop = {}

# State of the user for control the interactions while waiting the entry
user_state = {}


def set_user_state(chat_id, state):
    user_state[chat_id] = state


def get_user_state(chat_id):
    return user_state.get(chat_id)


# This is the data of the products
productos = {"Llavero":
             {"precio": 125, "imagen": "./assets/llaveros.jpg",
                 "texto": LLAVEROS_TEXT, "stock": "DISPONIBLE"},
             "Agenda": {"precio": 100, "imagen": "./assets/agendas.jpg", "texto": AGENDAS_TEXT, "stock": "DISPONIBLE"},
             "Calcomanía": {"precio": 30, "imagen": "./assets/calcomanías.jpg",
                            "texto": STICKERS_TEXT, "stock": "AGOTADO"},
             "Chibi": {"precio": 150, "imagen": "./assets/chibi.jpg", "texto": CHIBI_TEXT, "stock": "DISPONIBLE"},
             "Poster3D": {"precio": 150, "imagen": "./assets/poster3D.jpg", "texto": POSTER3D_TEXT, "stock": "DISPONIBLE"},
             "Figuras de acción": {"precio": 300, "imagen": "./assets/action_figures.jpg",
                                   "texto": ACTION_FIGURES_TEXT, "stock": "AGOTADO"},
             "Poster": {"precio": 50, "imagen": "./assets/poster.jpg", "texto": POSTERS_TEXT, "stock": "DISPONIBLE"},
             }
