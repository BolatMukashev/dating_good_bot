from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Ciao, <b>{first_name}</b>!\n"
                        "Pronto a fare nuove conoscenze?\n\n"
                        "Per iniziare devi completare alcuni semplici passaggi:\n\n"
                        "🔸 Passaggio 1. Premendo «Inizia registrazione» tu:"
                        "\n🔹 Confermi di avere almeno 18 anni 🪪"
                        '\n🔹 Accetti il <a href="{notion_site}">Contratto di utilizzo</a>'
                        '\n🔹 Accetti la <a href="{notion_site}">Politica sulla privacy</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Passaggio 2. Invia la tua posizione 🛰️\n\n"
                        "<i>La ricerca sarà effettuata tra le persone della tua città e del tuo Paese 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Passaggio 3. Scegli il tuo genere ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Passaggio 4. Indica chi stai cercando ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Passaggio 5. Invia la tua foto 🤳"
                        "\n<i>Preferibilmente un selfie, dove il volto sia ben visibile</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Passaggio 6. Racconta un po’ di te 📝"
                        "\n<i>Cerca di scrivere in breve — 2-3 righe</i>",
                        
                        "username_error": "⚠️ Per usare il bot è necessario impostare un <b>username</b> su Telegram."
                        "\nCome fare:"
                        "\n1️⃣ Apri Telegram → Impostazioni → Nome utente (tg://settings/username)"
                        "\n2️⃣ Scegli un <b>Nome utente</b> unico"
                        "\n3️⃣ Salva le modifiche ✅"
                        "\nDopo torna al bot e premi «Ripeti registrazione»",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passaggio 6 non completato"
                        "\nMinimo — {MIN_COUNT_SYMBOLS} caratteri"
                        "\nHai scritto — {text_length} caratteri"
                        "\nProva ad aggiungere qualcosa e invia di nuovo",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passaggio 6 non completato."
                        "\nSuperato il limite: massimo — {MAX_COUNT_SYMBOLS} caratteri."
                        "\nHai scritto — {text_length} caratteri."
                        "\nProva a ridurre il testo e invia di nuovo",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nSu di me: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Se usi Telegram da computer, completa questo passaggio dal tuo smartphone</i>",
                        "waiting": "In attesa ...",
                        },
       
        "notifications":{"18year":"Perfetto! Hai confermato di avere più di 18 anni",
                         "gender": "Perfetto! Hai indicato: {user_gender}",
                         "gender_search": "Perfetto! Hai indicato: {gender_search}",
                         "not_found": "Al momento non è stato trovato nessuno nella tua zona 😔",
                         "not_username": "Nome utente mancante ❌",
                         "reloaded": "Menu aggiornato 🔄",
                         "empty": "Non trovato",
                         "LOVE": "Vuoi un appuntamento con {name}",
                         "SEX": "Vuoi {name}",
                         "CHAT": "Vuoi chiacchierare con {name}",
                         "SKIP": "Hai saltato {name}",
                         "delete": "Utente eliminato ❌",
                         "payment_sent": "Pagamento inviato ⭐️",
                         "unavailable": "L’account {name} non è al momento disponibile 🚫",
                         "incognito" : {
                             True: "Modalità Incognito attivata ✅",
                             False: "Modalità Incognito disattivata 🚫"},
                         },
        "match_menu":{"start": "Qui puoi vedere:"
                      "\n🔹 Corrispondenze - i vostri desideri coincidono"
                      "\n🔹 Collezione - hai sbloccato l’accesso a queste persone"
                      "\n🔹 Reazioni di altre persone al tuo profilo",
                      "you_want": "Entrambi volete {reaction}",
                      "empty": {"LOVE": "Qui appariranno le persone che vogliono uscire con te a ☕ un <b>Appuntamento</b>",
                                "SEX": "Qui appariranno le persone che vogliono andare a letto con te 👩‍❤️‍💋‍👨 <b>Intimità</b>",
                                "CHAT": "Qui appariranno le persone che vogliono avere 💬 <b>Conversazione</b> con te"},
                      "match_empty": "Qui appariranno le persone con cui i vostri desideri coincidono"
                                    "\nPotrai scrivere loro ✉️",
                      "collection_empty": "La collezione è vuota"
                                           "\nAggiungi profili alla collezione ✨."
                                           "\nAlle persone della collezione puoi scrivere ✉️"},
        "search_menu":{"start": "🔍 Trova un partner",
                       "not_found": "Al momento non è stato trovato nessuno nella tua zona 😔"
                       "\nRiprova più tardi ☕"},
        "payment": {"incognito":{"label": "Attiva la modalità Incognito",
                                 "title": "Attiva la modalità Incognito",
                                "description": "Paghi una volta sola — e puoi attivare/disattivare quando vuoi!"
                                "\nIn questa modalità non sei visibile nella ricerca, ma puoi vedere i profili degli altri."},

                    "collection": {"label": "Aggiungi {target_name} alla ✨ Collezione",
                                   "title": "Aggiungi {target_name} alla ✨ Collezione",
                                   "description": "Aggiungendo alla ✨ Collezione, avrai accesso al profilo di {target_name} e potrai scriverle/gli" }
        }}


BUTTONS_TEXT = {"begin":"Inizia registrazione ✅",
                "reload": "Aggiorna 🔄",
                "back":"⬅️ Indietro",
                "next":"Avanti ➡️",
                "return":"⏮️ Torna al menu",
                "delete": "🗑️ Elimina profilo",
                "search_menu": {"start":"🔍 Inizia ricerca"
                                },
                "pay": "Paga con Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Appuntamento",
                             "SEX":"🔥 Intimità",
                             "CHAT": "💬 Conversazione",
                             "SKIP":"Salta ⏩"},
                "match_menu":{"start":"💘 Guarda corrispondenze",
                              "match":"💘 Corrispondenze [{match_count}]",
                              "collection":"✨ Collezione [{collection_count}]",
                              "love":"Appuntamento [{love_count}]",
                              "sex":"Intimità [{sex_count}]",
                              "chat":"Conversazione [{chat_count}]",
                              "add_to_collection":"Aggiungi alla Collezione {amount} ⭐️",
                              "send_message":"✉️ Invia messaggio"},
                "gender": {"man": "Ragazzo 🧔🏻",
                           "woman":"Ragazza 👩🏻‍🦰",
                           "any":"Altro 👱"},
                "gender_search": {"man": "Cerco un ragazzo 🧔🏻",
                                  "woman":"Cerco una ragazza 👩🏻‍🦰",
                                  "any":"Il genere non è importante 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Diventa Incognito",
                             "on":"✅ Incognito attivato",
                             "off":"🚫 Incognito disattivato",
                             },
                "profile":{"edit":"✏ Modifica profilo",
                           "retry":"🔄 Ripeti registrazione"},
                "location":{"send":"📍 Invia posizione",
                            "press":"📍 Premi per inviare"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Ragazzo 🧔🏻",
    Gender.WOMAN: "Ragazza 👩🏻‍🦰",
    Gender.ANY: "Altro 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Cerco un ragazzo 🧔🏻",
    Gender.WOMAN: "Cerco una ragazza 👩🏻‍🦰",
    Gender.ANY: "Il genere non è importante 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
