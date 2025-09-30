from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hola, <b>{first_name}</b>!\n"
                        "Preparat per a noves coneixences?\n\n"
                        "Per començar cal fer uns quants passos senzills:\n\n"
                        "🔸 Pas 1. En prémer «Començar el registre» tu:"
                        "\n🔹Confirms que ja tens 18 anys 🪪"
                        '\n🔹Acceptes les <a href="{notion_site}">Condicions d’ús</a>'
                        '\n🔹Acceptes la <a href="{notion_site}">Política de privacitat</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Pas 2. Envia la teva ubicació 🛰️\n\n"
                        "<i>La cerca es farà entre persones de la teva ciutat i país 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Pas 3. Tria el teu gènere ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Pas 4. Indica a qui busques ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Pas 5. Envia la teva <b>FOTO</b> 📎"
                        "\n<i>Preferiblement un selfie on es vegi bé la cara 🤳</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Pas 6. Explica una mica sobre tu 📝"
                        "\n<i>Escriu breu — 2-3 línies</i>",
                        
                        "username_error": "⚠️ Per utilitzar el bot, cal establir un <b>nom d’usuari</b> a Telegram."
                        "\nCom fer-ho:"
                        "\n1️⃣ Obre Telegram → Configuració → Nom d’usuari (tg://settings/username)"
                        "\n2️⃣ Tria un <b>nom d’usuari</b> únic"
                        "\n3️⃣ Desa els canvis ✅"
                        "\nDesprés torna al bot i prem «Tornar a registrar»",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ El pas 6 no s’ha completat"
                        "\nMínim — {MIN_COUNT_SYMBOLS} caràcters"
                        "\nTens — {text_length} caràcters"
                        "\nProva d’afegir més i torna a enviar-ho",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ El pas 6 no s’ha completat."
                        "\nLímit superat: màxim — {MAX_COUNT_SYMBOLS} caràcters."
                        "\nTens — {text_length} caràcters."
                        "\nProva de reduir el text i torna a enviar-ho",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nSobre mi: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Si fas servir Telegram a l’ordinador, completa aquest pas al mòbil</i>",
                        "waiting": "Esperant ...",
                        },
       
        "notifications":{"18year":"Perfecte! Has confirmat que tens més de 18 anys",
                         "gender": "Perfecte! Has indicat: {user_gender}",
                         "gender_search": "Perfecte! Has indicat: {gender_search}",
                         "not_found": "De moment no s’ha trobat ningú a la teva zona 😔",
                         "not_username": "Falta nom d’usuari ❌",
                         "reloaded": "Menú actualitzat 🔄",
                         "empty": "No s’ha trobat res",
                         "LOVE": "Vols una cita amb {name}",
                         "SEX": "Vols {name}",
                         "CHAT": "Vols xerrar amb {name}",
                         "SKIP": "Has saltat {name}",
                         "delete": "Usuari eliminat ❌",
                         "payment_sent": "Pagament enviat ⭐️",
                         "unavailable": "El compte de {name} no està disponible 🚫",
                         "incognito" : {
                             True: "Mode Incògnit activat ✅",
                             False: "Mode Incògnit desactivat 🚫"},
                         },
        "match_menu":{"start": "Aquí pots veure:"
                      "\n🔹 Coincidències - els vostres desitjos coincideixen"
                      "\n🔹 Col·lecció - tens accés per parlar amb aquestes persones"
                      "\n🔹 Reaccions d’altres usuaris al teu perfil",
                      "you_want": "Tots dos voleu {reaction}",
                      "empty": {"LOVE": "Aquí apareixeran persones que vulguin anar a una ☕ <b>Cita</b> amb tu",
                                "SEX": "Aquí apareixeran persones que vulguin anar amb tu al 🔥 <b>Llit</b>",
                                "CHAT": "Aquí apareixeran persones que vulguin 💬 <b>Xerrar</b> amb tu"},
                      "match_empty": "Aquí apareixeran persones amb qui coincideixin els vostres desitjos"
                                    "\nEls podràs escriure ✉️",
                      "collection_empty": "La col·lecció és buida"
                                           "\nAfegeix perfils a la col·lecció ✨."
                                           "\nA les persones de la col·lecció els pots escriure ✉️"},
        "search_menu":{"start": "🔍 Trobar parella",
                       "not_found": "De moment no s’ha trobat ningú a la teva zona 😔"
                       "\nTorna-ho a provar més tard ☕"},
        "payment": {"incognito":{"label": "Activa el mode Incògnit",
                                 "title": "Activa el mode Incògnit",
                                "description": "Compra’l una vegada i activa/desactiva quan vulguis!"
                                "\nEn aquest mode no et veuen a la cerca, però pots mirar perfils dels altres."},

                    "collection": {"label": "Afegeix {target_name} a ✨ Col·lecció",
                                   "title": "Afegeix {target_name} a ✨ Col·lecció",
                                   "description": "En afegir a la ✨ Col·lecció, tindràs accés al perfil de {target_name} i podràs escriure-li"}
        }}


BUTTONS_TEXT = {"begin":"Començar ✅",
                "reload": "Actualitzar 🔄",
                "back":"⬅️ Enrere",
                "next":"Següent ➡️",
                "return":"⏮️ Tornar al menú",
                "delete": "🗑️ Esborrar perfil",
                "search_menu": {"start":"🔍 Buscar"},
                "pay": "Pagar amb Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Cita",
                             "SEX":"🔥 Llit",
                             "CHAT": "💬 Xat",
                             "SKIP":"Saltar ⏩"},
                "match_menu":{"start":"💘 Coincidències",
                              "match":"💘 Coincidències [{match_count}]",
                              "collection":"✨ Col·lecció [{collection_count}]",
                              "love":"Cites [{love_count}]",
                              "sex":"Llit [{sex_count}]",
                              "chat":"Xats [{chat_count}]",
                              "add_to_collection":"Afegir a Col·lecció {amount} ⭐️",
                              "send_message":"✉️ Escriure"},
                "gender": {"man": "Noi 🧔🏻",
                           "woman":"Noia 👩🏻‍🦰",
                           "any":"Altres 👱"},
                "gender_search": {"man": "Busco noi 🧔🏻",
                                  "woman":"Busco noia 👩🏻‍🦰",
                                  "any":"Gènere indiferent 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Ser Incògnit",
                             "on":"✅ Incògnit activat",
                             "off":"🚫 Incògnit desactivat",
                             },
                "profile":{"edit":"✏ Editar perfil",
                           "retry":"🔄 Repetir registre"},
                "location":{"send":"📍 Enviar ubicació",
                            "press":"📍 Prem per enviar"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Noi 🧔🏻",
    Gender.WOMAN: "Noia 👩🏻‍🦰",
    Gender.ANY: "Altres 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Busco noi 🧔🏻",
    Gender.WOMAN: "Busco noia 👩🏻‍🦰",
    Gender.ANY: "Gènere indiferent 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
