from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Živjo, <b>{first_name}</b>!\n"
                        "Pripravljen na nova poznanstva?\n\n"
                        "Za začetek je treba opraviti nekaj preprostih korakov:\n\n"
                        "🔸 Korak 1. S klikom na »Začni registracijo« ti:"
                        "\n🔹Potrjuješ, da si star vsaj 18 let 🪪"
                        '\n🔹Sprejemaš <a href="{notion_site}">Uporabniški sporazum</a>'
                        '\n🔹Se strinjaš s <a href="{notion_site}">Politiko zasebnosti</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Korak 2. Pošlji svojo lokacijo 🛰️\n\n"
                        "<i>Iskanje bo potekalo med ljudmi iz tvojega mesta in države 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Korak 3. Izberi svoj spol ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Korak 4. Povej, koga iščeš ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Korak 5. Pošlji svojo fotografijo 🤳"
                        "\n<i>Priporočljivo je selfi, kjer se jasno vidi obraz</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Korak 6. Povej nekaj o sebi 📝"
                        "\n<i>Poskusi na kratko — 2–3 stavke</i>",
                        
                        "username_error": "⚠️ Za uporabo bota moraš nastaviti <b>uporabniško ime</b> v Telegramu."
                        "\nKako to storiti:"
                        "\n1️⃣ Odpri Telegram → Nastavitve → Uporabniško ime (tg://settings/username)"
                        "\n2️⃣ Izberi edinstveno <b>uporabniško ime</b>"
                        "\n3️⃣ Shrani spremembe ✅"
                        "\nNato se vrni v bota in klikni »Ponovi registracijo«",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Korak 6 ni opravljen"
                        "\nMinimalno — {MIN_COUNT_SYMBOLS} znakov"
                        "\nTi imaš — {text_length} znakov"
                        "\nPoskusi dodati več in pošlji znova",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Korak 6 ni opravljen."
                        "\nPresežena meja: največ — {MAX_COUNT_SYMBOLS} znakov."
                        "\nTi imaš — {text_length} znakov."
                        "\nPoskusi skrajšati opis in pošlji znova",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO sebi: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Če uporabljaš Telegram na računalniku, ta korak opravi na mobilni napravi</i>",
                        "waiting": "Čakanje ...",
                        },
       
        "notifications":{"18year":"Odlično! Potrdil si, da si starejši od 18 let",
                         "gender": "Odlično! Izbral si: {user_gender}",
                         "gender_search": "Odlično! Navedel si: {gender_search}",
                         "not_found": "Za zdaj ni nikogar v tvoji regiji 😔",
                         "not_username": "Manjka uporabniško ime ❌",
                         "reloaded": "Meni je osvežen 🔄",
                         "empty": "Ni najdeno",
                         "LOVE": "Želiš iti na zmenek z {name}",
                         "SEX": "Želiš {name}",
                         "CHAT": "Želiš se pogovarjati z {name}",
                         "SKIP": "Preskočil si {name}",
                         "delete": "Uporabnik izbrisan ❌",
                         "payment_sent": "Plačilo poslano ⭐️",
                         "unavailable": "Račun {name} trenutno ni dostopen 🚫",
                         "incognito" : {
                             True: "Način Incognito je vključen ✅",
                             False: "Način Incognito je izključen 🚫"},
                         },
        "match_menu":{"start": "Tu lahko pogledaš:"
                      "\n🔹 Ujemanja – vajine želje so se ujemale"
                      "\n🔹 Kolekcijo – dostop imaš do teh oseb"
                      "\n🔹 Reakcije drugih na tvoj profil",
                      "you_want": "Oba si želita {reaction}",
                      "empty": {"LOVE": "Tu se bodo prikazali ljudje, ki želijo zmenek ☕ <b>Zmenek</b>",
                                "SEX": "Tu se bodo prikazali ljudje, ki želijo s tabo v 👩‍❤️‍💋‍👨 <b>Posteljo</b>",
                                "CHAT": "Tu se bodo prikazali ljudje, ki želijo 💬 <b>Klepet</b> s tabo"},
                      "match_empty": "Tu bodo ljudje, s katerimi se vaše želje ujemajo"
                                    "\nLahko jim pošlješ sporočilo ✉️",
                      "collection_empty": "Kolekcija je prazna"
                                           "\nDodajaj profile v kolekcijo ✨."
                                           "\nTem ljudem lahko pošlješ sporočilo ✉️"},
        "search_menu":{"start": "🔍 Najdi partnerja",
                       "not_found": "Za zdaj ni nikogar v tvoji regiji 😔"
                       "\nPoskusi kasneje ☕"},
        "payment": {"incognito":{"label": "Aktiviraj način Incognito",
                                 "title": "Aktiviraj način Incognito",
                                "description": "Kupi enkrat — in vključi/izključi, kadar želiš!"
                                "\nV tem načinu te ne vidijo v iskanju, a ti lahko gledaš druge profile."},

                    "collection": {"label": "Dodaj {target_name} v ✨ Kolekcijo",
                                   "title": "Dodaj {target_name} v ✨ Kolekcijo",
                                   "description": "Z dodajanjem v ✨ Kolekcijo dobiš dostop do profila {target_name} in mu/ji lahko pišeš"}}
        }


BUTTONS_TEXT = {"begin":"Začni registracijo ✅",
                "reload": "Osveži 🔄",
                "back":"⬅️ Nazaj",
                "next":"➡️ Naprej",
                "return":"⏮️ Nazaj v meni",
                "delete": "🗑️ Izbriši profil",
                "search_menu": {"start":"🔍 Začni iskanje"
                                },
                "pay": "Plačaj prek Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Zmenek",
                             "SEX":"🔥 Postelja",
                             "CHAT": "💬 Klepet",
                             "SKIP":"⏩ Preskoči"},
                "match_menu":{"start":"💘 Poglej ujemanja",
                              "match":"💘 Ujemanja [{match_count}]",
                              "collection":"✨ Kolekcija [{collection_count}]",
                              "love":"Zmenek [{love_count}]",
                              "sex":"Postelja [{sex_count}]",
                              "chat":"Klepet [{chat_count}]",
                              "add_to_collection":"Dodaj v Kolekcijo {amount} ⭐️",
                              "send_message":"✉️ Pošlji sporočilo"},
                "gender": {"man": "Fant 🧔🏻",
                           "woman":"Punca 👩🏻‍🦰",
                           "any":"Drugo 👱"},
                "gender_search": {"man": "Iščem fanta 🧔🏻",
                                  "woman":"Iščem punco 👩🏻‍🦰",
                                  "any":"Spol ni pomemben 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Postani Incognito",
                             "on":"✅ Incognito vključen",
                             "off":"🚫 Incognito izključen",
                             },
                "profile":{"edit":"✏ Uredi profil",
                           "retry":"🔄 Ponovi registracijo"},
                "location":{"send":"📍 Pošlji lokacijo",
                            "press":"📍 Klikni za pošiljanje"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Fant 🧔🏻",
    Gender.WOMAN: "Punca 👩🏻‍🦰",
    Gender.ANY: "Drugo 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Iščem fanta 🧔🏻",
    Gender.WOMAN: "Iščem punco 👩🏻‍🦰",
    Gender.ANY: "Spol ni pomemben 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
