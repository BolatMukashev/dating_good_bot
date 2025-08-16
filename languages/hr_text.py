from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Bok, <b>{first_name}</b>!\n"
                        "Spreman za nova poznanstva?\n\n"
                        "Da bi počeo, trebaš napraviti par jednostavnih koraka:\n\n"
                        "🔸 Korak 1. Klikom na „Započni registraciju“ ti:"
                        "\n🔹Potvrđuješ da imaš 18+ godina 🪪"
                        '\n🔹Prihvaćaš <a href="{notion_site}">Uvjeti korištenja</a>'
                        '\n🔹Slažeš se s <a href="{notion_site}">Politika privatnosti</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Korak 2. Pošalji svoju lokaciju 🛰️\n\n"
                        "<i>Pretraga će biti među ljudima iz tvog grada i države 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Korak 3. Odaberi svoj spol ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Korak 4. Odaberi koga tražiš ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Korak 5. Pošalji svoju fotku 🤳"
                        "\n<i>Najbolje selfie gdje se jasno vidi lice</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Korak 6. Napiši nešto o sebi 📝"
                        "\n<i>Pokušaj kratko — 2-3 rečenice</i>",
                        
                        "username_error": "⚠️ Za korištenje bota moraš postaviti <b>username</b> u Telegramu."
                        "\nKako to napraviti:"
                        "\n1️⃣ Otvori Telegram → Postavke → Korisničko ime (tg://settings/username)"
                        "\n2️⃣ Smisli jedinstveno <b>Korisničko ime</b>"
                        "\n3️⃣ Spremi promjene ✅"
                        "\nZatim se vrati u bota i klikni \"Ponovi registraciju\"",


                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Korak 6 nije ispunjen"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} znakova"
                        "\nTvoj tekst ima {text_length} znakova"
                        "\nPokušaj nadopuniti opis i pošalji opet",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Korak 6 nije ispunjen."
                        "\nPreviše teksta: maksimum — {MAX_COUNT_SYMBOLS} znakova."
                        "\nTvoj tekst ima — {text_length} znakova."
                        "\nPokušaj skratiti opis i pošalji opet",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO meni: <i>{about_me}</i>",

                        "get_location_message": "<i>Ako koristiš Telegram na računalu, ovaj korak odradi na mobitelu</i>",
                        "waiting": "Čekanje ...",
                        },
       
        "notifications":{"18year":"Super! Potvrdio si da imaš 18+",
                         "gender": "Super! Označio si: {user_gender}",
                         "gender_search": "Super! Označio si: {gender_search}",
                         "not_found": "Trenutno nema nikoga u tvojoj regiji 😔",
                         "not_username": "Nema korisničkog imena ❌",
                         "reloaded": "Izbornik osvježen 🔄",
                         "empty": "Nema rezultata",
                         "LOVE": "Želiš na spoj s {name}",
                         "SEX": "Želiš {name}",
                         "CHAT": "Želiš pričati s {name}",
                         "SKIP": "Preskočio si {name}",
                         "delete": "Korisnik obrisan ❌",
                         "payment_sent": "Plaćanje poslano ⭐️",
                         "unavailable": "Račun {name} trenutno nije dostupan 🚫",
                         "incognito" : {
                             True: "Incognito način uključen ✅",
                             False: "Incognito način isključen 🚫"},
                         },
        "match_menu":{"start": "Ovdje možeš vidjeti:"
                      "\n🔹 Poklapanja - vaši interesi se poklapaju"
                      "\n🔹 Kolekcija - otključao si pristup ovim ljudima"
                      "\n🔹 Reakcije drugih na tvoj profil",
                      "you_want": "Oboje želite {reaction}",
                      "empty": {"LOVE": "Ovdje će se pojaviti ljudi koji žele s tobom na ☕ <b>Spoj</b>",
                                "SEX": "Ovdje će se pojaviti ljudi koji žele s tobom u 👩‍❤️‍💋‍👨 <b>Krevet</b>",
                                "CHAT": "Ovdje će se pojaviti ljudi koji žele 💬 <b>Razgovor</b> s tobom"},
                      "match_empty": "Ovdje će biti ljudi s kojima se poklapate"
                                    "\nMožeš im pisati ✉️",
                      "collection_empty": "Kolekcija je prazna"
                                           "\nDodaj profile u kolekciju ✨."
                                           "\nLjudima iz kolekcije možeš pisati ✉️"},
        "search_menu":{"start": "🔍 Nađi partnera",
                       "not_found": "Trenutno nema nikoga u tvojoj regiji 😔"
                       "\nPokušaj kasnije ☕"},
        "payment": {"incognito":{"label": "Aktiviraj Incognito",
                                 "title": "Aktiviraj Incognito način",
                                "description": "Kupi jednom — i pali/gasi kad želiš!"
                                "\nU ovom načinu te nema u pretrazi, ali ti možeš pregledavati profile drugih."},

                    "collection": {"label": "Dodaj {target_name} u ✨ Kolekcija",
                                   "title": "Dodaj {target_name} u ✨ Kolekcija",
                                   "description": "Dodavanjem u ✨ Kolekcija, dobivaš pristup profilu {target_name} i možeš mu/joj pisati"}
        }}


BUTTONS_TEXT = {"begin":"Započni ✅",
                "reload": "Osvježi 🔄",
                "back":"⬅️ Natrag",
                "next":"Dalje ➡️",
                "return":"⏮️ Izbornik",
                "delete": "🗑️ Obriši profil",
                "search_menu": {"start":"🔍 Traži"},
                "pay": "Plati preko Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Spoj",
                             "SEX":"🔥 Krevet",
                             "CHAT": "💬 Pričaj",
                             "SKIP":"Preskoči ⏩"},
                "match_menu":{"start":"💘 Pogledaj poklapanja",
                              "match":"💘 Poklapanja [{match_count}]",
                              "collection":"✨ Kolekcija [{collection_count}]",
                              "love":"Spoj [{love_count}]",
                              "sex":"Krevet [{sex_count}]",
                              "chat":"Razgovor [{chat_count}]",
                              "add_to_collection":"Dodaj u Kolekciju {amount} ⭐️",
                              "send_message":"✉️ Piši poruku"},
                "gender": {"man": "Muškarac 🧔🏻",
                           "woman":"Žena 👩🏻‍🦰",
                           "any":"Drugo 👱"},
                "gender_search": {"man": "Tražim muškarca 🧔🏻",
                                  "woman":"Tražim ženu 👩🏻‍🦰",
                                  "any":"Nije bitno 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Postani Incognito",
                             "on":"✅ Incognito uključen",
                             "off":"🚫 Incognito isključen",
                             },
                "profile":{"edit":"✏ Uredi profil",
                           "retry":"🔄 Ponovi registraciju"},
                "location":{"send":"📍 Pošalji lokaciju",
                            "press":"📍 Klikni za slanje"}
                }


GENDER_LABELS = {
    Gender.MAN: "Muškarac 🧔🏻",
    Gender.WOMAN: "Žena 👩🏻‍🦰",
    Gender.ANY: "Drugo 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Tražim muškarca 🧔🏻",
    Gender.WOMAN: "Tražim ženu 👩🏻‍🦰",
    Gender.ANY: "Nije bitno 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
