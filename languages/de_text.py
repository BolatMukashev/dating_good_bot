from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hallo, <b>{first_name}</b>!\n"
                        "Bereit für neue Kontakte?\n\n"
                        "Um loszulegen, musst du ein paar einfache Schritte machen:\n\n"
                        "🔸 Schritt 1. Mit „Registrierung starten“ bestätigst du:"
                        "\n🔹Du bist mindestens 18 Jahre alt 🪪"
                        '\n🔹Du akzeptierst die <a href="{notion_site}">Nutzungsbedingungen</a>'
                        '\n🔹Du stimmst der <a href="{notion_site}">Datenschutzrichtlinie</a> zu',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Schritt 2. Teile deinen Standort 🛰️\n\n"
                        "<i>Die Suche erfolgt unter Leuten aus deiner Stadt und deinem Land 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Schritt 3. Wähle dein Geschlecht ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Schritt 4. Wen suchst du? ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Schritt 5. Lade dein Foto hoch 🤳"
                        "\n<i>Am besten ein Selfie, auf dem dein Gesicht gut zu sehen ist</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Schritt 6. Erzähl ein bisschen über dich 📝"
                        "\n<i>Halte es kurz – 2-3 Sätze</i>",
                        
                        "username_error": "⚠️ Um den Bot zu nutzen, musst du einen <b>Benutzernamen</b> in Telegram festlegen."
                        "\nSo geht’s:"
                        "\n1️⃣ Öffne Telegram → Einstellungen → Benutzername (tg://settings/username)"
                        "\n2️⃣ Wähle einen eindeutigen <b>Benutzernamen</b>"
                        "\n3️⃣ Änderungen speichern ✅"
                        "\nDanach zurück zum Bot und „Registrierung wiederholen“ klicken",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Schritt 6 nicht abgeschlossen"
                        "\nMindestens — {MIN_COUNT_SYMBOLS} Zeichen"
                        "\nDu hast — {text_length} Zeichen"
                        "\nBitte ergänze deine Beschreibung und sende sie erneut",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Schritt 6 nicht abgeschlossen."
                        "\nLimit überschritten: maximal — {MAX_COUNT_SYMBOLS} Zeichen."
                        "\nDu hast — {text_length} Zeichen."
                        "\nBitte kürze deine Beschreibung und sende sie erneut",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nÜber mich: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Falls du Telegram am PC nutzt, mache diesen Schritt bitte auf deinem Handy</i>",
                        "waiting": "Warten ...",
                        },
       
        "notifications":{"18year":"Perfekt! Du hast bestätigt, dass du über 18 bist",
                         "gender": "Super! Du hast angegeben: {user_gender}",
                         "gender_search": "Super! Du suchst: {gender_search}",
                         "not_found": "Momentan niemand in deiner Region gefunden 😔",
                         "not_username": "Kein Benutzername gesetzt ❌",
                         "reloaded": "Menü aktualisiert 🔄",
                         "empty": "Nichts gefunden",
                         "LOVE": "Du willst ein Date mit {name}",
                         "SEX": "Du willst Intimität mit {name}",
                         "CHAT": "Du möchtest mit {name} chatten",
                         "SKIP": "Du hast {name} übersprungen",
                         "delete": "Nutzer gelöscht ❌",
                         "payment_sent": "Zahlung gesendet ⭐️",
                         "unavailable": "Account {name} ist gerade nicht verfügbar 🚫",
                         "incognito" : {
                             True: "Inkognito-Modus aktiviert ✅",
                             False: "Inkognito-Modus deaktiviert 🚫"},
                         },
        "match_menu":{"start": "Hier kannst du sehen:"
                      "\n🔹 Matches – eure Wünsche passen zusammen"
                      "\n🔹 Sammlung – du hast Zugriff auf diese Profile"
                      "\n🔹 Reaktionen anderer auf dein Profil",
                      "you_want": "Ihr beide wollt {reaction}",
                      "empty": {"LOVE": "Hier erscheinen Leute, die mit dir auf ein ☕ <b>Date</b> wollen",
                                "SEX": "Hier erscheinen Leute, die mit dir 🔥 <b>Intim</b> wollen",
                                "CHAT": "Hier erscheinen Leute, die 💬 <b>Chatten</b> möchten"},
                      "match_empty": "Hier erscheinen Leute, mit denen eure Wünsche übereinstimmen"
                                    "\nDu kannst ihnen schreiben ✉️",
                      "collection_empty": "Sammlung ist leer"
                                           "\nFüge Profile zur Sammlung hinzu ✨."
                                           "\nDiesen Leuten kannst du schreiben ✉️"},
        "search_menu":{"start": "🔍 Partner finden",
                       "not_found": "Momentan niemand in deiner Region gefunden 😔"
                       "\nVersuch es später noch einmal ☕"},
        "payment": {"incognito":{"label": "Inkognito-Modus aktivieren",
                                 "title": "Inkognito-Modus aktivieren",
                                "description": "Einmal kaufen — beliebig an- und ausschalten!"
                                "\nIn diesem Modus bist du unsichtbar in der Suche, kannst aber Profile anderer sehen."},

                    "collection": {"label": "{target_name} zu ✨ Sammlung hinzufügen",
                                   "title": "{target_name} zu ✨ Sammlung hinzufügen ",
                                   "description": "Mit dem Hinzufügen erhältst du Zugriff auf {target_name} und kannst ihr/ihm schreiben"}}
}


BUTTONS_TEXT = {"begin":"Start ✅",
                "reload": "Aktualisieren 🔄",
                "back":"⬅️ Zurück",
                "next":"Weiter ➡️",
                "return":"⏮️ Zurück ins Menü",
                "delete": "🗑️ Profil löschen",
                "search_menu": {"start":"🔍 Suche starten"
                                },
                "pay": "Mit Telegram Stars zahlen ⭐️",
                "reaction": {"LOVE":"☕ Date",
                             "SEX":"🔥 Intim",
                             "CHAT": "💬 Chat",
                             "SKIP":"Überspringen ⏩"},
                "match_menu":{"start":"💘 Matches ansehen",
                              "match":"💘 Matches [{match_count}]",
                              "collection":"✨ Sammlung [{collection_count}]",
                              "love":"Dates [{love_count}]",
                              "sex":"Intim [{sex_count}]",
                              "chat":"Chats [{chat_count}]",
                              "add_to_collection":"Zu Sammlung hinzufügen {amount} ⭐️",
                              "send_message":"Schreiben ✉️"},
                "gender": {"man": "Mann 🧔🏻",
                           "woman":"Frau 👩🏻‍🦰",
                           "any":"Andere 👱"},
                "gender_search": {"man": "Suche Mann 🧔🏻",
                                  "woman":"Suche Frau 👩🏻‍🦰",
                                  "any":"Geschlecht egal 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Inkognito werden",
                             "on":"✅ Inkognito an",
                             "off":"🚫 Inkognito aus",
                             },
                "profile":{"edit":"✏ Profil bearbeiten",
                           "retry":"🔄 Registrierung wiederholen"},
                "location":{"send":"📍 Standort senden",
                            "press":"📍 Zum Senden tippen"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Mann 🧔🏻",
    Gender.WOMAN: "Frau 👩🏻‍🦰",
    Gender.ANY: "Andere 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Suche Mann 🧔🏻",
    Gender.WOMAN: "Suche Frau 👩🏻‍🦰",
    Gender.ANY: "Geschlecht egal 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
