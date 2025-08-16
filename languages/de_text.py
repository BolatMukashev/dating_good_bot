from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hallo, <b>{first_name}</b>!\n"
                        "Bereit für neue Bekanntschaften?\n\n"
                        "Um zu starten, musst du ein paar einfache Schritte machen:\n\n"
                        "🔸 Schritt 1. Mit Klick auf „Registrierung starten“ bestätigst du:"
                        "\n🔹Dass du mindestens 18 Jahre alt bist 🪪"
                        '\n🔹Dass du die <a href="{notion_site}">Nutzungsbedingungen</a> akzeptierst'
                        '\n🔹Dass du der <a href="{notion_site}">Datenschutzerklärung</a> zustimmst',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Schritt 2. Sende deinen Standort 🛰️\n\n"
                        "<i>Die Suche erfolgt unter Menschen aus deiner Stadt und deinem Land 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Schritt 3. Wähle dein Geschlecht ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Schritt 4. Gib an, wen du suchst ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Schritt 5. Sende dein Foto 🤳"
                        "\n<i>Am besten ein Selfie, auf dem dein Gesicht gut sichtbar ist</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Schritt 6. Erzähle ein wenig über dich 📝"
                        "\n<i>Versuche dich kurz zu halten — 2–3 Sätze</i>",
                        
                        "username_error": "⚠️ Um den Bot zu benutzen, musst du einen <b>Benutzernamen</b> in Telegram festlegen."
                        "\nSo geht’s:"
                        "\n1️⃣ Öffne Telegram → Einstellungen → Benutzername (tg://settings/username)"
                        "\n2️⃣ Überlege dir einen eindeutigen <b>Benutzernamen</b>"
                        "\n3️⃣ Speichere die Änderungen ✅"
                        "\nDanach kehre zurück zum Bot und drücke „Registrierung wiederholen“",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Schritt 6 nicht erfüllt"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} Zeichen"
                        "\nDu hast — {text_length} Zeichen"
                        "\nBitte ergänze deine Beschreibung und sende sie erneut",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Schritt 6 nicht erfüllt."
                        "\nLimit überschritten: maximal — {MAX_COUNT_SYMBOLS} Zeichen."
                        "\nDu hast — {text_length} Zeichen."
                        "\nBitte kürze deine Beschreibung und sende sie erneut",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nÜber mich: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Wenn du Telegram auf dem Computer nutzt, mache diesen Schritt bitte am Handy</i>",
                        "waiting": "Warte ...",
                        },
       
        "notifications":{"18year":"Super! Du hast bestätigt, dass du über 18 bist",
                         "gender": "Super! Du hast angegeben: {user_gender}",
                         "gender_search": "Super! Du hast angegeben: {gender_search}",
                         "not_found": "Zurzeit wurde niemand in deiner Region gefunden 😔",
                         "not_username": "Kein Benutzername festgelegt ❌",
                         "reloaded": "Menü aktualisiert 🔄",
                         "empty": "Nichts gefunden",
                         "LOVE": "Du möchtest ein Date mit {name}",
                         "SEX": "Du möchtest Sex mit {name}",
                         "CHAT": "Du möchtest mit {name} chatten",
                         "SKIP": "Du hast {name} übersprungen",
                         "delete": "Benutzer gelöscht ❌",
                         "payment_sent": "Zahlung gesendet ⭐️",
                         "unavailable": "Das Konto von {name} ist gerade nicht verfügbar 🚫",
                         "incognito" : {
                             True: "Inkognito-Modus aktiviert ✅",
                             False: "Inkognito-Modus deaktiviert 🚫"},
                         },
        "match_menu":{"start": "Hier kannst du sehen:"
                      "\n🔹 Übereinstimmungen – eure Wünsche haben sich gedeckt"
                      "\n🔹 Sammlung – du hast Zugriff auf diese Profile"
                      "\n🔹 Reaktionen anderer Leute auf dein Profil",
                      "you_want": "Ihr beide wollt {reaction}",
                      "empty": {"LOVE": "Hier erscheinen Leute, die mit dir auf ein ☕ <b>Date</b> gehen wollen",
                                "SEX": "Hier erscheinen Leute, die mit dir 👩‍❤️‍💋‍👨 <b>Sex</b> haben wollen",
                                "CHAT": "Hier erscheinen Leute, die mit dir 💬 <b>Chatten</b> wollen"},
                      "match_empty": "Hier erscheinen Leute, mit denen sich eure Wünsche gedeckt haben"
                                    "\nDu kannst ihnen schreiben ✉️",
                      "collection_empty": "Sammlung ist leer"
                                           "\nFüge Profile zur Sammlung hinzu ✨."
                                           "\nDen Leuten aus der Sammlung kannst du schreiben ✉️"},
        "search_menu":{"start": "🔍 Partner finden",
                       "not_found": "Zurzeit wurde niemand in deiner Region gefunden 😔"
                       "\nVersuche es später noch einmal ☕"},
        "payment": {"incognito":{"label": "Inkognito-Modus aktivieren",
                                 "title": "Inkognito-Modus aktivieren",
                                "description": "Einmal kaufen — und ein-/ausschalten, wann du willst!"
                                "\nIn diesem Modus bist du in der Suche unsichtbar, kannst aber die Profile anderer ansehen."},

                    "collection": {"label": "{target_name} zu ✨ Sammlung hinzufügen",
                                   "title": "{target_name} zu ✨ Sammlung hinzufügen",
                                   "description": "Wenn du {target_name} zu ✨ Sammlung hinzufügst, erhältst du Zugriff auf sein/ihr Profil und kannst schreiben"}
        }}


BUTTONS_TEXT = {"begin":"Registrierung starten ✅",
                "reload": "Aktualisieren 🔄",
                "back":"⬅️ Zurück",
                "next":"Weiter ➡️",
                "return":"⏮️ Zurück zum Menü",
                "delete": "🗑️ Profil löschen",
                "search_menu": {"start":"🔍 Suche starten"
                                },
                "pay": "Mit Telegram Stars bezahlen ⭐️",
                "reaction": {"LOVE":"☕ Date",
                             "SEX":"🔥 Sex",
                             "CHAT": "💬 Chat",
                             "SKIP":"Überspringen ⏩"},
                "match_menu":{"start":"💘 Übereinstimmungen ansehen",
                              "match":"💘 Übereinstimmungen [{match_count}]",
                              "collection":"✨ Sammlung [{collection_count}]",
                              "love":"Date [{love_count}]",
                              "sex":"Sex [{sex_count}]",
                              "chat":"Chat [{chat_count}]",
                              "add_to_collection":"Zur Sammlung hinzufügen {amount} ⭐️",
                              "send_message":"✉️ Nachricht senden"},
                "gender": {"man": "Mann 🧔🏻",
                           "woman":"Frau 👩🏻‍🦰",
                           "any":"Anderes 👱"},
                "gender_search": {"man": "Ich suche einen Mann 🧔🏻",
                                  "woman":"Ich suche eine Frau 👩🏻‍🦰",
                                  "any":"Geschlecht egal 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Inkognito werden",
                             "on":"✅ Inkognito aktiviert",
                             "off":"🚫 Inkognito deaktiviert",
                             },
                "profile":{"edit":"✏ Profil bearbeiten",
                           "retry":"🔄 Registrierung wiederholen"},
                "location":{"send":"📍 Standort senden",
                            "press":"📍 Drücken, um zu senden"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Mann 🧔🏻",
    Gender.WOMAN: "Frau 👩🏻‍🦰",
    Gender.ANY: "Anderes 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Ich suche einen Mann 🧔🏻",
    Gender.WOMAN: "Ich suche eine Frau 👩🏻‍🦰",
    Gender.ANY: "Geschlecht egal 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
