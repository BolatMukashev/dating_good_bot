from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "¡Hola, <b>{first_name}</b>!\n"
                        "¿Listo para nuevas amistades? 🤝\n\n"
                        "Para empezar, debes completar unos pasos sencillos:\n\n"
                        "🔸 Paso 1. Al pulsar «Comenzar registro» tú:"
                        "\n🔹Confirmas que tienes más de 18 años 🪪"
                        '\n🔹Aceptas el <a href="{notion_site}">Acuerdo de Usuario</a>'
                        '\n🔹Aceptas la <a href="{notion_site}">Política de Privacidad</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Paso 2. Envía tu ubicación 🛰️\n\n"
                        "<i>La búsqueda se realizará entre personas de tu ciudad y país 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Paso 3. Elige tu género ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Paso 4. Indica a quién estás buscando ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Paso 5. Envía tu foto 🤳"
                        "\n<i>Preferiblemente un selfie donde se vea bien tu rostro</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Paso 6. Cuéntanos un poco sobre ti 📝"
                        "\n<i>Procura escribir breve — 2-3 líneas</i>",
                        
                        "username_error": "⚠️ Para usar el bot, necesitas configurar un <b>username</b> en Telegram."
                        "\nCómo hacerlo:"
                        "\n1️⃣ Abre Telegram → Ajustes → Nombre de usuario (tg://settings/username)"
                        "\n2️⃣ Crea un <b>nombre de usuario</b> único"
                        "\n3️⃣ Guarda los cambios ✅"
                        "\nDespués vuelve al bot y pulsa «Reintentar registro»",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Paso 6 no completado"
                        "\nMínimo — {MIN_COUNT_SYMBOLS} caracteres"
                        "\nTú has escrito — {text_length} caracteres"
                        "\nIntenta ampliar la descripción y envíala de nuevo",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Paso 6 no completado."
                        "\nLímite superado: máximo — {MAX_COUNT_SYMBOLS} caracteres."
                        "\nTú has escrito — {text_length} caracteres."
                        "\nIntenta resumir tu descripción y envíala de nuevo",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nSobre mí: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Si usas Telegram en computadora, completa este paso en un dispositivo móvil</i>",
                        "waiting": "Esperando ...",
                        },
       
        "notifications":{"18year":"¡Perfecto! Has confirmado que tienes más de 18 años",
                         "gender": "¡Perfecto! Has indicado: {user_gender}",
                         "gender_search": "¡Perfecto! Has indicado: {gender_search}",
                         "not_found": "Por ahora no se ha encontrado a nadie en tu región 😔",
                         "not_username": "Nombre de usuario ausente ❌",
                         "reloaded": "Menú actualizado 🔄",
                         "empty": "No encontrado",
                         "LOVE": "Quieres tener una cita con {name}",
                         "SEX": "Quieres intimidad con {name}",
                         "CHAT": "Quieres conversar con {name}",
                         "SKIP": "Has saltado a {name}",
                         "delete": "Usuario eliminado ❌",
                         "payment_sent": "Pago enviado ⭐️",
                         "unavailable": "La cuenta de {name} no está disponible 🚫",
                         "incognito" : {
                             True: "Modo Incógnito activado ✅",
                             False: "Modo Incógnito desactivado 🚫"},
                         },
        "match_menu":{"start": "Aquí puedes ver:"
                      "\n🔹 Coincidencias — sus intereses coinciden"
                      "\n🔹 Colección — tienes acceso para conversar con estas personas"
                      "\n🔹 Reacciones de otras personas a tu perfil",
                      "you_want": "Ambos quieren {reaction}",
                      "empty": {"LOVE": "Aquí aparecerán personas que quieren tener una ☕ <b>Cita</b> contigo",
                                "SEX": "Aquí aparecerán personas que quieren estar contigo en 👩‍❤️‍💋‍👨 <b>Intimidad</b>",
                                "CHAT": "Aquí aparecerán personas que quieren 💬 <b>Conversar</b> contigo"},
                      "match_empty": "Aquí aparecerán personas con las que coincidan tus intereses"
                                    "\nPodrás enviarles un mensaje ✉️",
                      "collection_empty": "La colección está vacía"
                                           "\nAgrega perfiles a la colección ✨."
                                           "\nA las personas de la colección puedes escribirles ✉️"},
        "search_menu":{"start": "🔍 Buscar pareja",
                       "not_found": "Por ahora no se ha encontrado a nadie en tu región 😔"
                       "\nIntenta más tarde ☕"},
        "payment": {"incognito":{"label": "Activar modo Incógnito",
                                 "title": "Activar modo Incógnito",
                                "description": "¡Compra una vez — y actívalo/desactívalo cuando quieras!"
                                "\nEn este modo no serás visible en la búsqueda, pero podrás ver perfiles de otros."},

                    "collection": {"label": "Agregar a {target_name} a ✨ Colección",
                                   "title": "Agregar a {target_name} a ✨ Colección",
                                   "description": "Al agregar a ✨ Colección, obtendrás acceso al perfil de {target_name} y podrás enviarle un mensaje"}
        }}


BUTTONS_TEXT = {"begin":"Comenzar registro ✅",
                "reload": "Actualizar 🔄",
                "back":"⬅️ Atrás",
                "next":"Siguiente ➡️",
                "return":"⏮️ Volver al menú",
                "delete": "🗑️ Eliminar perfil",
                "search_menu": {"start":"🔍 Iniciar búsqueda"
                                },
                "pay": "Pagar con Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Cita",
                             "SEX":"🔥 Intimidad",
                             "CHAT": "💬 Conversar",
                             "SKIP":"Saltar ⏩"},
                "match_menu":{"start":"💘 Ver coincidencias",
                              "match":"💘 Coincidencias [{match_count}]",
                              "collection":"✨ Colección [{collection_count}]",
                              "love":"Cita [{love_count}]",
                              "sex":"Intimidad [{sex_count}]",
                              "chat":"Conversar [{chat_count}]",
                              "add_to_collection":"Agregar a la Colección {amount} ⭐️",
                              "send_message":"✉️ Enviar mensaje"},
                "gender": {"man": "Chico 🧔🏻",
                           "woman":"Chica 👩🏻‍🦰",
                           "any":"Otro 👱"},
                "gender_search": {"man": "Busco chico 🧔🏻",
                                  "woman":"Busco chica 👩🏻‍🦰",
                                  "any":"El género no importa 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Hacerme Incógnito",
                             "on":"✅ Incógnito activado",
                             "off":"🚫 Incógnito desactivado",
                             },
                "profile":{"edit":"✏ Editar perfil",
                           "retry":"🔄 Reintentar registro"},
                "location":{"send":"📍 Enviar ubicación",
                            "press":"📍 Pulsa para enviar"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Chico 🧔🏻",
    Gender.WOMAN: "Chica 👩🏻‍🦰",
    Gender.ANY: "Otro 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Busco chico 🧔🏻",
    Gender.WOMAN: "Busco chica 👩🏻‍🦰",
    Gender.ANY: "El género no importa 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
