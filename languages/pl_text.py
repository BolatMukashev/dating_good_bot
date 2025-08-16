from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Cześć, <b>{first_name}</b>!\n"
                        "Gotowy/a na nowe znajomości?\n\n"
                        "Aby zacząć, musisz wykonać kilka prostych kroków:\n\n"
                        "🔸 Krok 1. Klikając „Rozpocznij rejestrację” ty:"
                        "\n🔹Potwierdzasz, że masz ukończone 18 lat 🪪"
                        '\n🔹Akceptujesz <a href="{notion_site}">Regulamin</a>'
                        '\n🔹Zgadzasz się z <a href="{notion_site}">Polityką prywatności</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 2. Wyślij swoją lokalizację 🛰️\n\n"
                        "<i>Wyszukiwanie będzie prowadzone wśród osób z twojego miasta i kraju 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Krok 3. Wybierz swoją płeć ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Krok 4. Wskaż, kogo szukasz ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Krok 5. Wyślij swoje zdjęcie 🤳"
                        "\n<i>Najlepiej selfie, na którym dobrze widać twarz</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Krok 6. Napisz kilka słów o sobie 📝"
                        "\n<i>Postaraj się krótko — 2-3 zdania</i>",
                        
                        "username_error": "⚠️ Aby korzystać z bota, musisz ustawić <b>username</b> w Telegramie."
                        "\nJak to zrobić:"
                        "\n1️⃣ Otwórz Telegram → Ustawienia → Nazwa użytkownika (tg://settings/username)"
                        "\n2️⃣ Wymyśl unikalną <b>Nazwę użytkownika</b>"
                        "\n3️⃣ Zapisz zmiany ✅"
                        "\nNastępnie wróć do bota i kliknij „Powtórz rejestrację”",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nie został wykonany"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} znaków"
                        "\nMasz — {text_length} znaków"
                        "\nSpróbuj dopisać coś i wyślij ponownie",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Krok 6 nie został wykonany."
                        "\nPrzekroczono limit: maksymalnie — {MAX_COUNT_SYMBOLS} znaków."
                        "\nMasz — {text_length} znaków."
                        "\nSpróbuj skrócić opis i wyślij ponownie",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO mnie: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Jeśli używasz Telegrama na komputerze, wykonaj ten krok na urządzeniu mobilnym</i>",
                        "waiting": "Oczekiwanie ...",
                        },
       
        "notifications":{"18year":"Super! Potwierdziłeś, że masz więcej niż 18 lat",
                         "gender": "Świetnie! Podałeś: {user_gender}",
                         "gender_search": "Świetnie! Podałeś: {gender_search}",
                         "not_found": "Na razie nikogo nie znaleziono w twoim regionie 😔",
                         "not_username": "Brak nazwy użytkownika ❌",
                         "reloaded": "Menu zostało odświeżone 🔄",
                         "empty": "Nie znaleziono",
                         "LOVE": "Chcesz iść na randkę z {name}",
                         "SEX": "Chcesz {name}",
                         "CHAT": "Chcesz porozmawiać z {name}",
                         "SKIP": "Pominąłeś {name}",
                         "delete": "Użytkownik został usunięty ❌",
                         "payment_sent": "Płatność wysłana ⭐️",
                         "unavailable": "Konto {name} jest teraz niedostępne 🚫",
                         "incognito" : {
                             True: "Tryb Incognito włączony ✅",
                             False: "Tryb Incognito wyłączony 🚫"},
                         },
        "match_menu":{"start": "Tutaj możesz zobaczyć:"
                      "\n🔹 Dopasowania - wasze pragnienia się pokryły"
                      "\n🔹 Kolekcja - masz dostęp do tych profili"
                      "\n🔹 Reakcje innych osób na twoją ankietę",
                      "you_want": "Oboje chcecie {reaction}",
                      "empty": {"LOVE": "Tutaj pojawią się osoby, które chcą z tobą iść na ☕ <b>Randkę</b>",
                                "SEX": "Tutaj pojawią się osoby, które chcą z tobą do 👩‍❤️‍💋‍👨 <b>Łóżka</b>",
                                "CHAT": "Tutaj pojawią się osoby, które chcą 💬 <b>Rozmowy</b> z tobą"},
                      "match_empty": "Tutaj pojawią się osoby, z którymi wasze pragnienia się pokryły"
                                    "\nBędziesz mógł/mogła do nich napisać ✉️",
                      "collection_empty": "Kolekcja jest pusta"
                                           "\nDodawaj profile do kolekcji ✨."
                                           "\nOsobom z kolekcji możesz napisać ✉️"},
        "search_menu":{"start": "🔍 Znajdź partnera",
                       "not_found": "Na razie nikogo nie znaleziono w twoim regionie 😔"
                       "\nSpróbuj później ☕"},
        "payment": {"incognito":{"label": "Aktywuj tryb Incognito",
                                 "title": "Aktywuj tryb Incognito",
                                "description": "Kup raz — i włączaj/wyłączaj kiedy chcesz!"
                                "\nW tym trybie nie jesteś widoczny/a w wyszukiwaniach, ale możesz przeglądać profile innych."},

                    "collection": {"label": "Dodaj {target_name} do ✨ Kolekcji",
                                   "title": "Dodaj {target_name} do ✨ Kolekcji ",
                                   "description": "Dodając do ✨ Kolekcji, uzyskasz dostęp do profilu {target_name} i będziesz mógł/mogła napisać do niego/niej"}
        }}


BUTTONS_TEXT = {"begin":"Zacznij ✅",
                "reload": "Odśwież 🔄",
                "back":"⬅️ Wstecz",
                "next":"Dalej ➡️",
                "return":"⏮️ Powrót",
                "delete": "🗑️ Usuń profil",
                "search_menu": {"start":"🔍 Szukaj"},
                "pay": "Zapłać przez Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Randka",
                             "SEX":"🔥 Łóżko",
                             "CHAT":"💬 Rozmowa",
                             "SKIP":"⏩ Pomiń"},
                "match_menu":{"start":"💘 Dopasowania",
                              "match":"💘 Dopasowania [{match_count}]",
                              "collection":"✨ Kolekcja [{collection_count}]",
                              "love":"Randki [{love_count}]",
                              "sex":"Łóżko [{sex_count}]",
                              "chat":"Rozmowy [{chat_count}]",
                              "add_to_collection":"Dodaj do Kolekcji {amount} ⭐️",
                              "send_message":"✉️ Napisz"},
                "gender": {"man": "Facet 🧔🏻",
                           "woman":"Kobieta 👩🏻‍🦰",
                           "any":"Inne 👱"},
                "gender_search": {"man": "Szukam faceta 🧔🏻",
                                  "woman":"Szukam kobiety 👩🏻‍🦰",
                                  "any":"Płeć bez znaczenia 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Bądź incognito",
                             "on":"✅ Incognito włączone",
                             "off":"🚫 Incognito wyłączone",
                             },
                "profile":{"edit":"✏ Edytuj profil",
                           "retry":"🔄 Powtórz rejestrację"},
                "location":{"send":"📍 Wyślij lokalizację",
                            "press":"📍 Kliknij, aby wysłać"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Facet 🧔🏻",
    Gender.WOMAN: "Kobieta 👩🏻‍🦰",
    Gender.ANY: "Inne 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Szukam faceta 🧔🏻",
    Gender.WOMAN: "Szukam kobiety 👩🏻‍🦰",
    Gender.ANY: "Płeć bez znaczenia 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
