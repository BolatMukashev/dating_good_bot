from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hallo, <b>{first_name}</b>!\n"
                        "Klaar voor nieuwe ontmoetingen?\n\n"
                        "Om te beginnen moet je een paar eenvoudige stappen doorlopen:\n\n"
                        "🔸 Stap 1. Door op «Registratie starten» te klikken:"
                        "\n🔹Bevestig je dat je 18 jaar of ouder bent 🪪"
                        '\n🔹Accepteer je de <a href="{notion_site}">Gebruikersovereenkomst</a>'
                        '\n🔹Ga je akkoord met het <a href="{notion_site}">Privacybeleid</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Stap 2. Stuur je locatie 🛰️\n\n"
                        "<i>De zoekopdracht vindt plaats onder mensen uit jouw stad en land 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Stap 3. Kies je geslacht ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Stap 4. Geef aan wie je zoekt ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Stap 5. Stuur een foto van jezelf 🤳"
                        "\n<i>Bij voorkeur een selfie waarop je gezicht goed zichtbaar is</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Stap 6. Vertel kort iets over jezelf 📝"
                        "\n<i>Hou het kort — 2-3 zinnen</i>",
                        
                        "username_error": "⚠️ Om de bot te gebruiken, moet je een <b>gebruikersnaam</b> instellen in Telegram."
                        "\nHoe je dat doet:"
                        "\n1️⃣ Open Telegram → Instellingen → Gebruikersnaam (tg://settings/username)"
                        "\n2️⃣ Bedenk een unieke <b>gebruikersnaam</b>"
                        "\n3️⃣ Sla de wijzigingen op ✅"
                        "\nKom daarna terug naar de bot en druk op \"Registratie opnieuw starten\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Stap 6 niet voltooid"
                        "\nMinimaal — {MIN_COUNT_SYMBOLS} tekens"
                        "\nJouw tekst bevat {text_length} tekens"
                        "\nProbeer je beschrijving aan te vullen en stuur opnieuw",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Stap 6 niet voltooid."
                        "\nTe veel tekst: maximaal — {MAX_COUNT_SYMBOLS} tekens."
                        "\nJouw tekst bevat {text_length} tekens."
                        "\nProbeer het korter te maken en stuur opnieuw",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nOver mij: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Als je Telegram op je computer gebruikt, rond deze stap dan af op je mobiele apparaat</i>",
                        "waiting": "Even geduld ...",
                        },
       
        "notifications":{"18year":"Top! Je hebt bevestigd dat je ouder bent dan 18 jaar",
                         "gender": "Goed! Je hebt aangegeven: {user_gender}",
                         "gender_search": "Goed! Je zoekt: {gender_search}",
                         "not_found": "Er zijn momenteel geen mensen in jouw regio gevonden 😔",
                         "not_username": "Geen gebruikersnaam ingesteld ❌",
                         "reloaded": "Menu vernieuwd 🔄",
                         "empty": "Niets gevonden",
                         "LOVE": "Je wilt op date met {name}",
                         "SEX": "Je wilt intimiteit met {name}",
                         "CHAT": "Je wilt chatten met {name}",
                         "SKIP": "Je hebt {name} overgeslagen",
                         "delete": "Gebruiker verwijderd ❌",
                         "payment_sent": "Betaling verzonden ⭐️",
                         "unavailable": "Account {name} is momenteel niet beschikbaar 🚫",
                         "incognito" : {
                             True: "Incognito-modus ingeschakeld ✅",
                             False: "Incognito-modus uitgeschakeld 🚫"},
                         },
        "match_menu":{"start": "Hier kun je bekijken:"
                      "\n🔹 Matches - jullie wensen komen overeen"
                      "\n🔹 Collectie - je hebt toegang tot deze profielen"
                      "\n🔹 Reacties van anderen op jouw profiel",
                      "you_want": "Jullie willen allebei {reaction}",
                      "empty": {"LOVE": "Hier verschijnen mensen die met jou op een ☕ <b>Date</b> willen",
                                "SEX": "Hier verschijnen mensen die met jou naar bed 👩‍❤️‍💋‍👨 willen",
                                "CHAT": "Hier verschijnen mensen die 💬 <b>Willen praten</b> met jou"},
                      "match_empty": "Hier verschijnen mensen met wie jouw wensen overeenkomen"
                                    "\nJe kunt ze een bericht sturen ✉️",
                      "collection_empty": "De collectie is leeg"
                                           "\nVoeg profielen toe aan je collectie ✨."
                                           "\nJe kunt mensen uit je collectie een bericht sturen ✉️"},
        "search_menu":{"start": "🔍 Zoek een partner",
                       "not_found": "Er zijn momenteel geen mensen in jouw regio gevonden 😔"
                       "\nProbeer het later opnieuw ☕"},
        "payment": {"incognito":{"label": "Incognito-modus activeren",
                                 "title": "Incognito-modus activeren",
                                "description": "Koop één keer — en schakel aan/uit wanneer je wilt!"
                                "\nIn deze modus ben jij niet zichtbaar in de zoekresultaten, maar je kunt wel andere profielen bekijken."},

                    "collection": {"label": "Voeg {target_name} toe aan ✨ Collectie",
                                   "title": "Voeg {target_name} toe aan ✨ Collectie ",
                                   "description": "Door {target_name} toe te voegen aan ✨ Collectie, krijg je toegang tot hun profiel en kun je haar/hem een bericht sturen"}}
        }


BUTTONS_TEXT = {"begin":"Registratie starten ✅",
                "reload": "Vernieuwen 🔄",
                "back":"⬅️ Terug",
                "next":"Volgende ➡️",
                "return":"⏮️ Terug naar menu",
                "delete": "🗑️ Profiel verwijderen",
                "search_menu": {"start":"🔍 Zoek starten"
                                },
                "pay": "Betalen met Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Date",
                             "SEX":"🔥 Intiem",
                             "CHAT": "💬 Praten",
                             "SKIP":"Overslaan ⏩"},
                "match_menu":{"start":"💘 Bekijk matches",
                              "match":"💘 Matches [{match_count}]",
                              "collection":"✨ Collectie [{collection_count}]",
                              "love":"Date [{love_count}]",
                              "sex":"Intiem [{sex_count}]",
                              "chat":"Praten [{chat_count}]",
                              "add_to_collection":"Toevoegen aan Collectie {amount} ⭐️",
                              "send_message":"✉️ Bericht sturen"},
                "gender": {"man": "Man 🧔🏻",
                           "woman":"Vrouw 👩🏻‍🦰",
                           "any":"Anders 👱"},
                "gender_search": {"man": "Ik zoek een man 🧔🏻",
                                  "woman":"Ik zoek een vrouw 👩🏻‍🦰",
                                  "any":"Geslacht maakt niet uit 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Word Incognito",
                             "on":"✅ Incognito ingeschakeld",
                             "off":"🚫 Incognito uitgeschakeld",
                             },
                "profile":{"edit":"✏ Profiel bewerken",
                           "retry":"🔄 Registratie opnieuw starten"},
                "location":{"send":"📍 Locatie sturen",
                            "press":"📍 Druk om te sturen"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Man 🧔🏻",
    Gender.WOMAN: "Vrouw 👩🏻‍🦰",
    Gender.ANY: "Anders 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Ik zoek een man 🧔🏻",
    Gender.WOMAN: "Ik zoek een vrouw 👩🏻‍🦰",
    Gender.ANY: "Geslacht maakt niet uit 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
