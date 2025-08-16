from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Szia, <b>{first_name}</b>!\n"
                        "Készen állsz új ismeretségekre?\n\n"
                        "A kezdéshez néhány egyszerű lépést kell elvégezned:\n\n"
                        "🔸 1. lépés. A «Regisztráció indítása» gomb megnyomásával te:"
                        "\n🔹Megerősíted, hogy elmúltál 18 éves 🪪"
                        '\n🔹Elfogadod a <a href="{notion_site}">Felhasználási feltételeket</a>'
                        '\n🔹Beleegyezel az <a href="{notion_site}">Adatvédelmi szabályzatba</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 2. lépés. Küldd el a tartózkodási helyed 🛰️\n\n"
                        "<i>A keresés a városodban és az országodban élő emberek között fog történni 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 3. lépés. Válaszd ki a nemed ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 4. lépés. Add meg, kit keresel ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 5. lépés. Küldj magadról fotót 🤳"
                        "\n<i>Lehetőleg szelfit, ahol jól látszik az arcod</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 6. lépés. Mesélj kicsit magadról 📝"
                        "\n<i>Próbálj rövid lenni — 2-3 mondat</i>",
                        
                        "username_error": "⚠️ A bot használatához be kell állítanod a <b>felhasználóneved</b> a Telegramban."
                        "\nHogyan kell ezt megtenni:"
                        "\n1️⃣ Nyisd meg: Telegram → Beállítások → Felhasználónév (tg://settings/username)"
                        "\n2️⃣ Adj meg egy egyedi <b>Felhasználónevet</b>"
                        "\n3️⃣ Mentsd el a módosításokat ✅"
                        "\nEzután térj vissza a bothoz és nyomd meg az „Újraregisztráció” gombot.",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ A 6. lépés nem teljesült"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} karakter"
                        "\nNálad — {text_length} karakter"
                        "\nEgészítsd ki a leírásod, majd küldd el újra.",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ A 6. lépés nem teljesült."
                        "\nTúllépted a határt: maximum — {MAX_COUNT_SYMBOLS} karakter."
                        "\nNálad — {text_length} karakter."
                        "\nPróbáld rövidíteni a leírást, majd küldd el újra.",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nRólam: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Ha számítógépen használod a Telegramot, ezt a lépést mobilon végezd el</i>",
                        "waiting": "Várakozás ...",
                        },
       
        "notifications":{"18year":"Szuper! Megerősítetted, hogy elmúltál 18 éves",
                         "gender": "Szuper! Megadtad: {user_gender}",
                         "gender_search": "Szuper! Megadtad: {gender_search}",
                         "not_found": "Egyelőre senkit sem találtunk a környékeden 😔",
                         "not_username": "Nincs felhasználónév beállítva ❌",
                         "reloaded": "Menü frissítve 🔄",
                         "empty": "Nem található",
                         "LOVE": "Randira mennél vele: {name}",
                         "SEX": "Szeretnél együtt lenni vele: {name}",
                         "CHAT": "Beszélgetni szeretnél vele: {name}",
                         "SKIP": "Kihagytad: {name}",
                         "delete": "Felhasználó törölve ❌",
                         "payment_sent": "Fizetés elküldve ⭐️",
                         "unavailable": "{name} fiókja most nem elérhető 🚫",
                         "incognito" : {
                             True: "Inkog­nító mód bekapcsolva ✅",
                             False: "Inkog­nító mód kikapcsolva 🚫"},
                         },
        "match_menu":{"start": "Itt megnézheted:"
                      "\n🔹 Találatok – ahol az igényeitek egyeznek"
                      "\n🔹 Gyűjtemény – azok, akikkel már írhatsz"
                      "\n🔹 Mások reakciói a profilodra",
                      "you_want": "Mindketten szeretnétek: {reaction}",
                      "empty": {"LOVE": "Itt jelennek meg azok, akik veled szeretnének elmenni egy ☕ <b>Randira</b>",
                                "SEX": "Itt jelennek meg azok, akik veled szeretnének 👩‍❤️‍💋‍👨 <b>Közeli kapcsolatot</b>",
                                "CHAT": "Itt jelennek meg azok, akik veled szeretnének 💬 <b>Beszélgetni</b>"},
                      "match_empty": "Itt jelennek meg azok, akikkel egyeztek az igényeitek"
                                    "\nÍrhatsz nekik ✉️",
                      "collection_empty": "A gyűjtemény üres"
                                           "\nAdj hozzá profilokat ✨."
                                           "\nA gyűjteményben lévőknek írhatsz ✉️"},
        "search_menu":{"start": "🔍 Partner keresése",
                       "not_found": "Egyelőre senkit sem találtunk a környékeden 😔"
                       "\nPróbáld meg később ☕"},
        "payment": {"incognito":{"label": "Inkog­nító mód aktiválása",
                                 "title": "Inkog­nító mód aktiválása",
                                "description": "Egyszeri vásárlás — és bármikor ki/be kapcsolhatod!"
                                "\nEbben a módban nem látnak a keresésben, de te megnézheted mások profilját."},

                    "collection": {"label": "Hozzáadás a ✨ Gyűjteményhez: {target_name}",
                                   "title": "Add hozzá {target_name}-t a ✨ Gyűjteményhez",
                                   "description": "Ha hozzáadod a ✨ Gyűjteményhez, hozzáférést kapsz {target_name} profiljához és írhatsz neki."}
        }}


BUTTONS_TEXT = {"begin":"Regisztráció ✅",
                "reload": "Frissít 🔄",
                "back":"⬅️ Vissza",
                "next":"Tovább ➡️",
                "return":"⏮️ Menübe",
                "delete": "🗑️ Profil törlése",
                "search_menu": {"start":"🔍 Keresés"},
                "pay": "Fizetés Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Randi",
                             "SEX":"🔥 Közeli kapcsolat",
                             "CHAT":"💬 Csevegés",
                             "SKIP":"Kihagy ⏩"},
                "match_menu":{"start":"💘 Találatok",
                              "match":"💘 Találatok [{match_count}]",
                              "collection":"✨ Gyűjtemény [{collection_count}]",
                              "love":"Randik [{love_count}]",
                              "sex":"Kapcsolatok [{sex_count}]",
                              "chat":"Beszélgetés [{chat_count}]",
                              "add_to_collection":"Gyűjtemény {amount} ⭐️",
                              "send_message":"✉️ Üzenet írása"},
                "gender": {"man": "Férfi 🧔🏻",
                           "woman":"Nő 👩🏻‍🦰",
                           "any":"Más 👱"},
                "gender_search": {"man": "Férfit keresek 🧔🏻",
                                  "woman":"Nőt keresek 👩🏻‍🦰",
                                  "any":"Mindegy 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Inkog­nító",
                             "on":"✅ Inkog­nító aktív",
                             "off":"🚫 Inkog­nító ki"},
                "profile":{"edit":"✏ Profil szerk.",
                           "retry":"🔄 Újrakezdés"},
                "location":{"send":"📍 Hely elküldése",
                            "press":"📍 Küldés"}
                }


GENDER_LABELS = {
    Gender.MAN: "Férfi 🧔🏻",
    Gender.WOMAN: "Nő 👩🏻‍🦰",
    Gender.ANY: "Más 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Férfit keresek 🧔🏻",
    Gender.WOMAN: "Nőt keresek 👩🏻‍🦰",
    Gender.ANY: "Mindegy 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
