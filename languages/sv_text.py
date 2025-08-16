from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hej, <b>{first_name}</b>!\n"
                        "Redo för nya bekantskaper?\n\n"
                        "För att börja behöver du göra några enkla steg:\n\n"
                        "🔸 Steg 1. När du trycker på «Starta registrering» så:"
                        "\n🔹Bekräftar du att du är minst 18 år 🪪"
                        '\n🔹Accepterar du <a href="{notion_site}">Användarvillkoren</a>'
                        '\n🔹Godkänner du <a href="{notion_site}">Integritetspolicyn</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Steg 2. Skicka din plats 🛰️\n\n"
                        "<i>Sökningen sker bland personer i din stad och ditt land 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Steg 3. Välj ditt kön ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Steg 4. Ange vem du söker ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Steg 5. Skicka ett foto 🤳"
                        "\n<i>Helst en selfie där ansiktet syns tydligt</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Steg 6. Berätta lite om dig själv 📝"
                        "\n<i>Försök att skriva kort — 2-3 rader</i>",
                        
                        "username_error": "⚠️ För att använda boten måste du ställa in ett <b>användarnamn</b> i Telegram."
                        "\nSå här gör du:"
                        "\n1️⃣ Öppna Telegram → Inställningar → Användarnamn (tg://settings/username)"
                        "\n2️⃣ Hitta på ett unikt <b>Användarnamn</b>"
                        "\n3️⃣ Spara ändringarna ✅"
                        "\nKom sedan tillbaka till boten och tryck \"Upprepa registrering\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Steg 6 är inte klart"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} tecken"
                        "\nDu skrev {text_length} tecken"
                        "\nFörsök att skriva lite mer och skicka igen",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Steg 6 är inte klart."
                        "\nÖverskriden gräns: max — {MAX_COUNT_SYMBOLS} tecken."
                        "\nDu skrev {text_length} tecken."
                        "\nFörsök att korta ner och skicka igen",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nOm mig: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Om du använder Telegram på dator, gör detta steg i mobilen</i>",
                        "waiting": "Väntar ...",
                        },
       
        "notifications":{"18year":"Perfekt! Du har bekräftat att du är över 18 år",
                         "gender": "Perfekt! Du angav: {user_gender}",
                         "gender_search": "Perfekt! Du söker: {gender_search}",
                         "not_found": "Det finns ingen i ditt område just nu 😔",
                         "not_username": "Inget användarnamn ❌",
                         "reloaded": "Menyn uppdaterad 🔄",
                         "empty": "Inget hittat",
                         "LOVE": "Du vill gå på dejt med {name}",
                         "SEX": "Du vill ha intimitet med {name}",
                         "CHAT": "Du vill chatta med {name}",
                         "SKIP": "Du hoppade över {name}",
                         "delete": "Användaren raderades ❌",
                         "payment_sent": "Betalningen skickades ⭐️",
                         "unavailable": "Kontot {name} är inte tillgängligt just nu 🚫",
                         "incognito" : {
                             True: "Inkognitoläge aktiverat ✅",
                             False: "Inkognitoläge avstängt 🚫"},
                         },
        "match_menu":{"start": "Här kan du se:"
                      "\n🔹 Matchningar - era önskningar matchade"
                      "\n🔹 Samling - du har låst upp kontakt med dessa personer"
                      "\n🔹 Andras reaktioner på din profil",
                      "you_want": "Ni båda vill {reaction}",
                      "empty": {"LOVE": "Här dyker det upp personer som vill gå på ☕ <b>Dejt</b> med dig",
                                "SEX": "Här dyker det upp personer som vill ha 👩‍❤️‍💋‍👨 <b>Intimitet</b> med dig",
                                "CHAT": "Här dyker det upp personer som vill ha 💬 <b>Samtal</b> med dig"},
                      "match_empty": "Här kommer personer upp som matchar dina önskningar"
                                    "\nDu kan skriva till dem ✉️",
                      "collection_empty": "Samlingen är tom"
                                           "\nLägg till profiler i samlingen ✨."
                                           "\nTill personer i samlingen kan du skriva ✉️"},
        "search_menu":{"start": "🔍 Hitta en partner",
                       "not_found": "Det finns ingen i ditt område just nu 😔"
                       "\nFörsök igen senare ☕"},
        "payment": {"incognito":{"label": "Aktivera Inkognitoläge",
                                 "title": "Aktivera Inkognitoläge",
                                "description": "Köp en gång — och slå på/av när du vill!"
                                "\nI det här läget syns du inte i sökningen, men du kan se andras profiler."},

                    "collection": {"label": "Lägg till {target_name} i ✨ Samling",
                                   "title": "Lägg till {target_name} i ✨ Samling ",
                                   "description": "När du lägger till i ✨ Samling får du tillgång till {target_name}s profil och kan skriva till henne/honom"}}
        }


BUTTONS_TEXT = {"begin":"Starta registrering ✅",
                "reload": "Uppdatera 🔄",
                "back":"⬅️ Tillbaka",
                "next":"Nästa ➡️",
                "return":"⏮️ Återvänd till menyn",
                "delete": "🗑️ Radera profil",
                "search_menu": {"start":"🔍 Starta sökning"
                                },
                "pay": "Betala via Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Dejt",
                             "SEX":"🔥 Intimitet",
                             "CHAT": "💬 Samtal",
                             "SKIP":"Hoppa över ⏩"},
                "match_menu":{"start":"💘 Se matchningar",
                              "match":"💘 Matchningar [{match_count}]",
                              "collection":"✨ Samling [{collection_count}]",
                              "love":"Dejter [{love_count}]",
                              "sex":"Intimitet [{sex_count}]",
                              "chat":"Samtal [{chat_count}]",
                              "add_to_collection":"Lägg till i Samling {amount} ⭐️",
                              "send_message":"✉️ Skicka meddelande"},
                "gender": {"man": "Kille 🧔🏻",
                           "woman":"Tjej 👩🏻‍🦰",
                           "any":"Annat 👱"},
                "gender_search": {"man": "Söker kille 🧔🏻",
                                  "woman":"Söker tjej 👩🏻‍🦰",
                                  "any":"Kön spelar ingen roll 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Bli Inkognito",
                             "on":"✅ Inkognito på",
                             "off":"🚫 Inkognito av",
                             },
                "profile":{"edit":"✏ Ändra profil",
                           "retry":"🔄 Upprepa registrering"},
                "location":{"send":"📍 Skicka plats",
                            "press":"📍 Tryck för att skicka"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Kille 🧔🏻",
    Gender.WOMAN: "Tjej 👩🏻‍🦰",
    Gender.ANY: "Annat 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Söker kille 🧔🏻",
    Gender.WOMAN: "Söker tjej 👩🏻‍🦰",
    Gender.ANY: "Kön spelar ingen roll 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
