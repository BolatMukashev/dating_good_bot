from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Ahoj, <b>{first_name}</b>!\n"
                        "Pripravený/á na nové zoznámenia?\n\n"
                        "Aby si začal/a, treba spraviť pár jednoduchých krokov:\n\n"
                        "🔸 Krok 1. Kliknutím na „Začať registráciu“ ty:"
                        "\n🔹Potvrdzuješ, že máš minimálne 18 rokov 🪪"
                        '\n🔹Súhlasíš s <a href="{notion_site}">Používateľskou dohodou</a>'
                        '\n🔹Súhlasíš s <a href="{notion_site}">Zásadami ochrany osobných údajov</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 2. Pošli svoju polohu 🛰️\n\n"
                        "<i>Vyhľadávanie bude prebiehať medzi ľuďmi z tvojho mesta a krajiny 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 3. Vyber si svoje pohlavie ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Krok 4. Uveď, koho hľadáš ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Krok 5. Pošli svoju fotku 🤳"
                        "\n<i>Najlepšie selfie, kde je dobre vidno tvár</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Krok 6. Napíš niečo o sebe 📝"
                        "\n<i>Snaž sa stručne — 2-3 vety</i>",
                        
                        "username_error": "⚠️ Na používanie bota je potrebné nastaviť si <b>username</b> v Telegrame."
                        "\nAko na to:"
                        "\n1️⃣ Otvor Telegram → Nastavenia → Používateľské meno (tg://settings/username)"
                        "\n2️⃣ Vymysli si jedinečné <b>Používateľské meno</b>"
                        "\n3️⃣ Ulož zmeny ✅"
                        "\nPotom sa vráť k botovi a klikni „Znova registrácia“",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nesplnený"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} znakov"
                        "\nTy máš - {text_length} znakov"
                        "\nSkús doplniť opis a pošli znova",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nesplnený."
                        "\nLimit prekročený: maximum — {MAX_COUNT_SYMBOLS} znakov."
                        "\nTy máš — {text_length} znakov."
                        "\nSkús skrátiť opis a pošli znova",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO mne: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Ak používaš Telegram na počítači, tento krok urob na mobile</i>",
                        "waiting": "Čakám ...",
                        },
       
        "notifications":{"18year":"Super! Potvrdil/a si, že máš viac než 18 rokov",
                         "gender": "Super! Uviedol/a si: {user_gender}",
                         "gender_search": "Super! Uviedol/a si: {gender_search}",
                         "not_found": "Zatiaľ sa v tvojom regióne nikto nenašiel 😔",
                         "not_username": "Chýba používateľské meno ❌",
                         "reloaded": "Menu obnovené 🔄",
                         "empty": "Nenašlo sa nič",
                         "LOVE": "Chceš ísť na rande s {name}",
                         "SEX": "Chceš {name}",
                         "CHAT": "Chceš sa porozprávať s {name}",
                         "SKIP": "Preskočil/a si {name}",
                         "delete": "Používateľ odstránený ❌",
                         "payment_sent": "Platba odoslaná ⭐️",
                         "unavailable": "Účet {name} nie je dostupný 🚫",
                         "incognito" : {
                             True: "Režim Inkognito zapnutý ✅",
                             False: "Režim Inkognito vypnutý 🚫"},
                         },
        "match_menu":{"start": "Tu si môžeš pozrieť:"
                      "\n🔹 Zhody - vaše želania sa zhodli"
                      "\n🔹 Kolekcia - máš prístup k týmto ľuďom"
                      "\n🔹 Reakcie iných na tvoj profil",
                      "you_want": "Obaja chcete {reaction}",
                      "empty": {"LOVE": "Tu budú ľudia, ktorí chcú ísť s tebou na ☕ <b>Rande</b>",
                                "SEX": "Tu budú ľudia, ktorí chcú s tebou do 👩‍❤️‍💋‍👨 <b>Postele</b>",
                                "CHAT": "Tu budú ľudia, ktorí chcú s tebou 💬 <b>Pokecať</b>"},
                      "match_empty": "Tu budú ľudia, s ktorými sa vaše želania zhodli"
                                    "\nMôžeš im napísať ✉️",
                      "collection_empty": "Kolekcia je prázdna"
                                           "\nPridávaj profily do kolekcie ✨."
                                           "\nĽuďom z kolekcie môžeš napísať ✉️"},
        "search_menu":{"start": "🔍 Nájsť partnera",
                       "not_found": "Zatiaľ sa nikto nenašiel 😔"
                       "\nSkús neskôr ☕"},
        "payment": {"incognito":{"label": "Aktivovať Inkognito",
                                 "title": "Aktivovať Inkognito",
                                "description": "Kúp raz — a zapínaj/vypínaj kedykoľvek!"
                                "\nV tomto režime ťa nikto neuvidí v hľadaní, ale ty môžeš prezerať profily."},

                    "collection": {"label": "Pridať {target_name} do ✨ Kolekcie",
                                   "title": "Pridať {target_name} do ✨ Kolekcie",
                                   "description": "Pridaním do ✨ Kolekcie získaš prístup k profilu {target_name} a môžeš jej/mu napísať"} 
        }}


BUTTONS_TEXT = {"begin":"Začať ✅",
                "reload": "Obnoviť 🔄",
                "back":"⬅️ Späť",
                "next":"Ďalej ➡️",
                "return":"⏮️ Menu",
                "delete": "🗑️ Zmazať profil",
                "search_menu": {"start":"🔍 Hľadať"},
                "pay": "Zaplatiť cez Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Rande",
                             "SEX":"🔥 Posteľ",
                             "CHAT":"💬 Pokec",
                             "SKIP":"Preskočiť ⏩"},
                "match_menu":{"start":"💘 Zhody",
                              "match":"💘 Zhody [{match_count}]",
                              "collection":"✨ Kolekcia [{collection_count}]",
                              "love":"Rande [{love_count}]",
                              "sex":"Posteľ [{sex_count}]",
                              "chat":"Pokec [{chat_count}]",
                              "add_to_collection":"Pridať do Kolekcie {amount} ⭐️",
                              "send_message":"✉️ Napísať"},
                "gender": {"man":"Chalan 🧔🏻",
                           "woman":"Dievča 👩🏻‍🦰",
                           "any":"Iné 👱"},
                "gender_search": {"man":"Hľadám chalana 🧔🏻",
                                  "woman":"Hľadám dievča 👩🏻‍🦰",
                                  "any":"Nezáleží 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Byť Inkognito",
                             "on":"✅ Inkognito zapnuté",
                             "off":"🚫 Inkognito vypnuté",
                             },
                "profile":{"edit":"✏ Upraviť profil",
                           "retry":"🔄 Znova registrácia"},
                "location":{"send":"📍 Poslať polohu",
                            "press":"📍 Klikni pre odoslanie"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Chalan 🧔🏻",
    Gender.WOMAN: "Dievča 👩🏻‍🦰",
    Gender.ANY: "Iné 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Hľadám chalana 🧔🏻",
    Gender.WOMAN: "Hľadám dievča 👩🏻‍🦰",
    Gender.ANY: "Nezáleží 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
