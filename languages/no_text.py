from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hei, <b>{first_name}</b>!\n"
                        "Klar for nye bekjentskaper?\n\n"
                        "For å starte må du gjøre noen enkle trinn:\n\n"
                        "🔸 Steg 1. Ved å trykke «Start registrering» så:"
                        "\n🔹Bekrefter du at du er over 18 år 🪪"
                        '\n🔹Godtar du <a href="{notion_site}">Brukeravtalen</a>'
                        '\n🔹Samtykker du til <a href="{notion_site}">Personvernerklæringen</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Steg 2. Send din posisjon 🛰️\n\n"
                        "<i>Søk vil skje blant folk i din by og ditt land 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Steg 3. Velg ditt kjønn ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Steg 4. Oppgi hvem du ser etter ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Steg 5. Send ditt bilde 🤳"
                        "\n<i>Helst en selfie der ansiktet ditt er godt synlig</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Steg 6. Fortell litt om deg selv 📝"
                        "\n<i>Prøv å skrive kort — 2–3 setninger</i>",
                        
                        "username_error": "⚠️ For å bruke boten må du ha satt et <b>brukernavn</b> i Telegram."
                        "\nSlik gjør du det:"
                        "\n1️⃣ Åpne Telegram → Innstillinger → Brukernavn (tg://settings/username)"
                        "\n2️⃣ Finn på et unikt <b>brukernavn</b>"
                        "\n3️⃣ Lagre endringene ✅"
                        "\nDeretter kan du gå tilbake til boten og trykke «Start registrering på nytt»",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Steg 6 er ikke fullført"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} tegn"
                        "\nDu skrev — {text_length} tegn"
                        "\nPrøv å skrive litt mer og send på nytt",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Steg 6 er ikke fullført"
                        "\nGrensen er overskredet: maks — {MAX_COUNT_SYMBOLS} tegn."
                        "\nDu skrev — {text_length} tegn."
                        "\nPrøv å forkorte teksten og send på nytt",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nOm meg: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Hvis du bruker Telegram på PC, gjør dette trinnet på mobilen</i>",
                        "waiting": "Venter ...",
                        },
       
        "notifications":{"18year":"Flott! Du har bekreftet at du er over 18 år",
                         "gender": "Flott! Du oppga: {user_gender}",
                         "gender_search": "Flott! Du oppga: {gender_search}",
                         "not_found": "Ingen funnet i ditt område ennå 😔",
                         "not_username": "Ingen brukernavn satt ❌",
                         "reloaded": "Menyen er oppdatert 🔄",
                         "empty": "Ikke funnet",
                         "LOVE": "Du vil på date med {name}",
                         "SEX": "Du ønsker {name}",
                         "CHAT": "Du ønsker å chatte med {name}",
                         "SKIP": "Du hoppet over {name}",
                         "delete": "Brukeren er slettet ❌",
                         "payment_sent": "Betaling sendt ⭐️",
                         "unavailable": "Kontoen {name} er ikke tilgjengelig nå 🚫",
                         "incognito" : {
                             True: "Inkognitomodus er slått på ✅",
                             False: "Inkognitomodus er slått av 🚫"},
                         },
        "match_menu":{"start": "Her kan du se:"
                      "\n🔹 Match – når ønskene deres er like"
                      "\n🔹 Favoritter – profiler du har åpnet tilgang til"
                      "\n🔹 Reaksjoner fra andre på din profil",
                      "you_want": "Dere begge vil {reaction}",
                      "empty": {"LOVE": "Her vil det dukke opp folk som vil gå på ☕ <b>Date</b> med deg",
                                "SEX": "Her vil det dukke opp folk som ønsker 🔥 <b>Intimitet</b> med deg",
                                "CHAT": "Her vil det dukke opp folk som vil ha 💬 <b>Samtale</b> med deg"},
                      "match_empty": "Her vil du se folk som deler dine ønsker"
                                    "\nDu kan sende dem melding ✉️",
                      "collection_empty": "Favoritter er tom"
                                           "\nLegg til profiler i favoritter ✨."
                                           "\nFolk i favoritter kan du sende melding til ✉️"},
        "search_menu":{"start": "🔍 Finn en partner",
                       "not_found": "Ingen funnet i ditt område ennå 😔"
                       "\nPrøv igjen senere ☕"},
        "payment": {"incognito":{"label": "Aktiver Inkognitomodus",
                                 "title": "Aktiver Inkognitomodus",
                                "description": "Kjøp én gang — og slå av/på når du vil!"
                                "\nI denne modusen er du usynlig i søk, men du kan selv se andres profiler."},

                    "collection": {"label": "Legg til {target_name} i ✨ Favoritter",
                                   "title": "Legg til {target_name} i ✨ Favoritter",
                                   "description": "Når du legger til i ✨ Favoritter, får du tilgang til {target_name} sin profil og kan sende melding"}
        }}


BUTTONS_TEXT = {"begin":"Start registrering ✅",
                "reload": "Oppdater 🔄",
                "back":"⬅️ Tilbake",
                "next":"Neste ➡️",
                "return":"⏮️ Tilbake til menyen",
                "delete": "🗑️ Slett profil",
                "search_menu": {"start":"🔍 Start søk"
                                },
                "pay": "Betal med Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Date",
                             "SEX":"🔥 Intimitet",
                             "CHAT": "💬 Samtale",
                             "SKIP":"Hopp over ⏩"},
                "match_menu":{"start":"💘 Se matcher",
                              "match":"💘 Matcher [{match_count}]",
                              "collection":"✨ Favoritter [{collection_count}]",
                              "love":"Date [{love_count}]",
                              "sex":"Intimitet [{sex_count}]",
                              "chat":"Samtale [{chat_count}]",
                              "add_to_collection":"Legg til i Favoritter {amount} ⭐️",
                              "send_message":"✉️ Send melding"},
                "gender": {"man": "Mann 🧔🏻",
                           "woman":"Kvinne 👩🏻‍🦰",
                           "any":"Annet 👱"},
                "gender_search": {"man": "Ser etter mann 🧔🏻",
                                  "woman":"Ser etter kvinne 👩🏻‍🦰",
                                  "any":"Kjønn spiller ingen rolle 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Bli Inkognito",
                             "on":"✅ Inkognito er på",
                             "off":"🚫 Inkognito er av",
                             },
                "profile":{"edit":"✏ Endre profil",
                           "retry":"🔄 Start registrering på nytt"},
                "location":{"send":"📍 Send posisjon",
                            "press":"📍 Trykk for å sende"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Mann 🧔🏻",
    Gender.WOMAN: "Kvinne 👩🏻‍🦰",
    Gender.ANY: "Annet 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Ser etter mann 🧔🏻",
    Gender.WOMAN: "Ser etter kvinne 👩🏻‍🦰",
    Gender.ANY: "Kjønn spiller ingen rolle 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
