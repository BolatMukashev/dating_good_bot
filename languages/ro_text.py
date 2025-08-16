from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Salut, <b>{first_name}</b>!\n"
                        "Ești gata pentru noi întâlniri? 😉\n\n"
                        "Pentru a începe, urmează câțiva pași simpli:\n\n"
                        "🔸 Pasul 1. Apăsând «Începe înregistrarea» tu:"
                        "\n🔹Confirmi că ai împlinit 18 ani 🪪"
                        '\n🔹Accepți <a href="{notion_site}">Acordul utilizatorului</a>'
                        '\n🔹Ești de acord cu <a href="{notion_site}">Politica de confidențialitate</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Pasul 2. Trimite-ți locația 🛰️\n\n"
                        "<i>Căutarea se va face printre persoane din orașul și țara ta 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Pasul 3. Alege-ți genul ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Pasul 4. Spune pe cine cauți ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Pasul 5. Trimite o poză 🤳"
                        "\n<i>De preferat un selfie unde se vede clar fața</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Pasul 6. Povestește puțin despre tine 📝"
                        "\n<i>Scrie scurt — 2-3 rânduri</i>",
                        
                        "username_error": "⚠️ Pentru a folosi botul, trebuie să ai setat un <b>username</b> în Telegram."
                        "\nCum se face:"
                        "\n1️⃣ Deschide Telegram → Setări → Nume utilizator (tg://settings/username)"
                        "\n2️⃣ Alege un <b>Nume unic</b>"
                        "\n3️⃣ Salvează ✅"
                        "\nApoi revino în bot și apasă \"Reia înregistrarea\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Pasul 6 nu este complet"
                        "\nMinim — {MIN_COUNT_SYMBOLS} caractere"
                        "\nTu ai — {text_length} caractere"
                        "\nAdaugă ceva și trimite din nou",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Pasul 6 nu este complet."
                        "\nAi depășit limita: maxim — {MAX_COUNT_SYMBOLS} caractere."
                        "\nTu ai — {text_length} caractere."
                        "\nRedu textul și trimite din nou",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nDespre mine: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Dacă folosești Telegram pe PC, fă acest pas de pe telefon</i>",
                        "waiting": "Așteaptă ...",
                        },
       
        "notifications":{"18year":"Perfect! Ai confirmat că ai peste 18 ani",
                         "gender": "Super! Ai selectat: {user_gender}",
                         "gender_search": "Super! Cauți: {gender_search}",
                         "not_found": "Momentan nu s-a găsit nimeni în zona ta 😔",
                         "not_username": "Nume utilizator lipsă ❌",
                         "reloaded": "Meniu actualizat 🔄",
                         "empty": "Nimic găsit",
                         "LOVE": "Vrei o întâlnire cu {name} ☕",
                         "SEX": "Îl/o vrei pe {name} 🔥",
                         "CHAT": "Vrei să vorbești cu {name} 💬",
                         "SKIP": "Ai sărit peste {name} ⏩",
                         "delete": "Profil șters ❌",
                         "payment_sent": "Plată trimisă ⭐️",
                         "unavailable": "Contul {name} nu este disponibil 🚫",
                         "incognito" : {
                             True: "Modul Incognito este activ ✅",
                             False: "Modul Incognito este dezactivat 🚫"},
                         },
        "match_menu":{"start": "Aici poți vedea:"
                      "\n🔹 Potriviri - dorințele voastre coincid"
                      "\n🔹 Colecția - ai acces la acești oameni"
                      "\n🔹 Reacțiile altora la profilul tău",
                      "you_want": "Amândoi vreți {reaction}",
                      "empty": {"LOVE": "Aici vor apărea persoane care vor ☕ <b>Întâlnire</b> cu tine",
                                "SEX": "Aici vor apărea persoane care vor 👩‍❤️‍💋‍👨 <b>Sex</b> cu tine",
                                "CHAT": "Aici vor apărea persoane care vor 💬 <b>Conversație</b>"},
                      "match_empty": "Aici vor apărea persoanele cu care dorințele voastre coincid"
                                    "\nLe vei putea scrie ✉️",
                      "collection_empty": "Colecția e goală"
                                           "\nAdaugă profiluri în colecție ✨."
                                           "\nCelor din colecție le poți scrie ✉️"},
        "search_menu":{"start": "🔍 Caută un partener",
                       "not_found": "Momentan nu s-a găsit nimeni în zona ta 😔"
                       "\nÎncearcă mai târziu ☕"},
        "payment": {"incognito":{"label": "Activează Incognito",
                                 "title": "Activează modul Incognito",
                                "description": "Cumperi o dată — și îl activezi/dezactivezi când vrei!"
                                "\nÎn acest mod nu apari în căutări, dar poți vedea tu profilurile altora."},

                    "collection": {"label": "Adaugă {target_name} în ✨ Colecție",
                                   "title": "Adaugă {target_name} în ✨ Colecție",
                                   "description": "Adăugând în ✨ Colecție, primești acces la profilul {target_name} și poți scrie direct"}
        }}


BUTTONS_TEXT = {"begin":"Înregistrare ✅",
                "reload": "Reîmprospătează 🔄",
                "back":"⬅️ Înapoi",
                "next":"➡️ Înainte",
                "return":"⏮️ Meniu",
                "delete": "🗑️ Șterge profilul",
                "search_menu": {"start":"🔍 Start căutare"},
                "pay": "Plătește cu Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Întâlnire",
                             "SEX":"🔥 Sex",
                             "CHAT": "💬 Chat",
                             "SKIP":"⏩ Sari"},
                "match_menu":{"start":"💘 Vezi potriviri",
                              "match":"💘 Potriviri [{match_count}]",
                              "collection":"✨ Colecție [{collection_count}]",
                              "love":"Întâlniri [{love_count}]",
                              "sex":"Sex [{sex_count}]",
                              "chat":"Chat [{chat_count}]",
                              "add_to_collection":"Adaugă în Colecție {amount} ⭐️",
                              "send_message":"✉️ Scrie mesaj"},
                "gender": {"man": "Băiat 🧔🏻",
                           "woman":"Fatã 👩🏻‍🦰",
                           "any":"Altceva 👱"},
                "gender_search": {"man": "Caut băiat 🧔🏻",
                                  "woman":"Caut fată 👩🏻‍🦰",
                                  "any":"Nu contează 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Fii Incognito",
                             "on":"✅ Incognito ON",
                             "off":"🚫 Incognito OFF",
                             },
                "profile":{"edit":"✏ Editează",
                           "retry":"🔄 Reia înregistrarea"},
                "location":{"send":"📍 Trimite locația",
                            "press":"📍 Apasă pentru a trimite"}
                }


GENDER_LABELS = {
    Gender.MAN: "Băiat 🧔🏻",
    Gender.WOMAN: "Fatã 👩🏻‍🦰",
    Gender.ANY: "Altceva 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Caut băiat 🧔🏻",
    Gender.WOMAN: "Caut fată 👩🏻‍🦰",
    Gender.ANY: "Nu contează 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
