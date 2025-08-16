from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Ahoj, <b>{first_name}</b>!\n"
                        "Připraven/a na nové seznámení?\n\n"
                        "Abychom mohli začít, je potřeba projít pár jednoduchých kroků:\n\n"
                        "🔸 Krok 1. Kliknutím na „Začít registraci“ zároveň:"
                        "\n🔹Potvrzuješ, že ti je minimálně 18 let 🪪"
                        '\n🔹Souhlasíš s <a href="{notion_site}">Uživatelskou smlouvou</a>'
                        '\n🔹Souhlasíš s <a href="{notion_site}">Zásadami ochrany osobních údajů</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 2. Pošli svou polohu 🛰️\n\n"
                        "<i>Vyhledávání probíhá mezi lidmi z tvého města a země 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 3. Vyber své pohlaví ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Krok 4. Uveď, koho hledáš ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Krok 5. Pošli svou fotku 🤳"
                        "\n<i>Nejlépe selfie, kde je dobře vidět tvůj obličej</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Krok 6. Napiš něco o sobě 📝"
                        "\n<i>Snaž se stručně — 2–3 věty</i>",
                        
                        "username_error": "⚠️ Pro použití bota je potřeba mít nastavený <b>username</b> v Telegramu."
                        "\nJak na to:"
                        "\n1️⃣ Otevři Telegram → Nastavení → Uživatelské jméno (tg://settings/username)"
                        "\n2️⃣ Vymysli si jedinečné <b>Uživatelské jméno</b>"
                        "\n3️⃣ Ulož změny ✅"
                        "\nPak se vrať k botovi a klikni „Opakovat registraci“",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nesplněn"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} znaků"
                        "\nMáš — {text_length} znaků"
                        "\nZkus text doplnit a pošli znovu",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nesplněn."
                        "\nPřekročen limit: maximum — {MAX_COUNT_SYMBOLS} znaků."
                        "\nMáš — {text_length} znaků."
                        "\nZkrať popis a pošli znovu",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO mně: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Pokud používáš Telegram na počítači, tento krok dokonči na mobilu</i>",
                        "waiting": "Čekám ...",
                        },
       
        "notifications":{"18year":"Super! Potvrdil/a jsi, že ti je více než 18 let",
                         "gender": "Super! Uvedl/a jsi: {user_gender}",
                         "gender_search": "Super! Hledáš: {gender_search}",
                         "not_found": "Zatím nikdo v tvém okolí 😔",
                         "not_username": "Chybí uživatelské jméno ❌",
                         "reloaded": "Menu aktualizováno 🔄",
                         "empty": "Nic nenalezeno",
                         "LOVE": "Chceš jít na rande s {name}",
                         "SEX": "Chceš {name}",
                         "CHAT": "Chceš si povídat s {name}",
                         "SKIP": "Přeskočil/a jsi {name}",
                         "delete": "Uživatel odstraněn ❌",
                         "payment_sent": "Platba odeslána ⭐️",
                         "unavailable": "Účet {name} není dostupný 🚫",
                         "incognito" : {
                             True: "Režim Inkognito zapnut ✅",
                             False: "Režim Inkognito vypnut 🚫"},
                         },
        "match_menu":{"start": "Tady si můžeš prohlédnout:"
                      "\n🔹 Shody – vaše přání se shodují"
                      "\n🔹 Kolekci – lidé, ke kterým máš přístup k chatu"
                      "\n🔹 Reakce ostatních na tvůj profil",
                      "you_want": "Oba chcete {reaction}",
                      "empty": {"LOVE": "Zde se objeví lidé, kteří chtějí jít s tebou na ☕ <b>Rande</b>",
                                "SEX": "Zde se objeví lidé, kteří chtějí s tebou do 👩‍❤️‍💋‍👨 <b>Postele</b>",
                                "CHAT": "Zde se objeví lidé, kteří chtějí 💬 <b>Pokec</b> s tebou"},
                      "match_empty": "Zde se objeví lidé, se kterými máte shodná přání"
                                    "\nBudeš jim moci napsat ✉️",
                      "collection_empty": "Kolekce je prázdná"
                                           "\nPřidávej profily do kolekce ✨."
                                           "\nLidem v kolekci můžeš napsat ✉️"},
        "search_menu":{"start": "🔍 Najít partnera",
                       "not_found": "Zatím nikdo v tvém okolí 😔"
                       "\nZkus to později ☕"},
        "payment": {"incognito":{"label": "Aktivovat Inkognito",
                                 "title": "Aktivovat režim Inkognito",
                                "description": "Kup jednou — a pak můžeš kdykoliv zapínat/vypínat!"
                                "\nV tomto režimu tě nikdo neuvidí ve vyhledávání, ale ty můžeš prohlížet profily jiných."},

                    "collection": {"label": "Přidat {target_name} do ✨ Kolekce",
                                   "title": "Přidat {target_name} do ✨ Kolekce",
                                   "description": "Přidáním do ✨ Kolekce získáš přístup k profilu {target_name} a můžeš jí/mu napsat"}}
}


BUTTONS_TEXT = {"begin":"Začít ✅",
                "reload": "Obnovit 🔄",
                "back":"⬅️ Zpět",
                "next":"➡️ Dál",
                "return":"⏮️ Menu",
                "delete": "🗑️ Smazat profil",
                "search_menu": {"start":"🔍 Hledat"},
                "pay": "Zaplatit přes Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Rande",
                             "SEX":"🔥 Postel",
                             "CHAT": "💬 Pokec",
                             "SKIP":"⏩ Přeskočit"},
                "match_menu":{"start":"💘 Shody",
                              "match":"💘 Shody [{match_count}]",
                              "collection":"✨ Kolekce [{collection_count}]",
                              "love":"Rande [{love_count}]",
                              "sex":"Postel [{sex_count}]",
                              "chat":"Pokec [{chat_count}]",
                              "add_to_collection":"Do Kolekce {amount} ⭐️",
                              "send_message":"✉️ Napsat"},
                "gender": {"man": "Kluk 🧔🏻",
                           "woman":"Holka 👩🏻‍🦰",
                           "any":"Jiné 👱"},
                "gender_search": {"man": "Hledám kluka 🧔🏻",
                                  "woman":"Hledám holku 👩🏻‍🦰",
                                  "any":"Na pohlaví nezáleží 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Být Inkognito",
                             "on":"✅ Inkognito zapnuto",
                             "off":"🚫 Inkognito vypnuto"},
                "profile":{"edit":"✏ Upravit profil",
                           "retry":"🔄 Opakovat registraci"},
                "location":{"send":"📍 Poslat polohu",
                            "press":"📍 Klikni pro poslání"}
                }


GENDER_LABELS = {
    Gender.MAN: "Kluk 🧔🏻",
    Gender.WOMAN: "Holka 👩🏻‍🦰",
    Gender.ANY: "Jiné 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Hledám kluka 🧔🏻",
    Gender.WOMAN: "Hledám holku 👩🏻‍🦰",
    Gender.ANY: "Na pohlaví nezáleží 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
