from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hei, <b>{first_name}</b>!\n"
                        "Valmis uusiin tuttavuuksiin? 💫\n\n"
                        "Aloittaaksesi sinun tarvitsee tehdä muutama yksinkertainen askel:\n\n"
                        "🔸 Vaihe 1. Painamalla «Aloita rekisteröinti» sinä:"
                        "\n🔹Vahvistat, että olet täyttänyt 18 vuotta 🪪"
                        '\n🔹Hyväksyt <a href="{notion_site}">Käyttöehdot</a>'
                        '\n🔹Hyväksyt myös <a href="{notion_site}">Tietosuojakäytännön</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Vaihe 2. Lähetä sijaintisi 🛰️\n\n"
                        "<i>Haku tehdään ihmisten keskuudessa kaupungissasi ja maassasi 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Vaihe 3. Valitse sukupuolesi ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Vaihe 4. Kerro, ketä etsit ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Vaihe 5. Lähetä kuvasi 🤳"
                        "\n<i>Mieluiten selfie, jossa kasvosi näkyvät hyvin</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Vaihe 6. Kerro hieman itsestäsi 📝"
                        "\n<i>Kirjoita lyhyesti — 2–3 riviä</i>",
                        
                        "username_error": "⚠️ Käyttääksesi bottia sinun täytyy asettaa <b>käyttäjänimi</b> Telegramissa."
                        "\nNäin teet sen:"
                        "\n1️⃣ Avaa Telegram → Asetukset → Käyttäjänimi (tg://settings/username)"
                        "\n2️⃣ Keksi uniikki <b>Käyttäjänimi</b>"
                        "\n3️⃣ Tallenna muutokset ✅"
                        "\nSen jälkeen palaa bottiin ja paina \"Aloita rekisteröinti uudelleen\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Vaihe 6 ei onnistunut"
                        "\nVähintään — {MIN_COUNT_SYMBOLS} merkkiä"
                        "\nSinulla on - {text_length} merkkiä"
                        "\nYritä täydentää kuvausta ja lähetä uudelleen",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Vaihe 6 ei onnistunut."
                        "\nRaja ylitetty: enintään — {MAX_COUNT_SYMBOLS} merkkiä."
                        "\nSinulla on — {text_length} merkkiä."
                        "\nYritä lyhentää kuvausta ja lähetä uudelleen",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nTietoa: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Jos käytät Telegramia tietokoneella, suorita tämä vaihe mobiililaitteella</i>",
                        "waiting": "Odotetaan ...",
                        },
       
        "notifications":{"18year":"Hienoa! Vahvistit, että olet yli 18-vuotias",
                         "gender": "Hienoa! Valitsit: {user_gender}",
                         "gender_search": "Hienoa! Valitsit: {gender_search}",
                         "not_found": "Alueeltasi ei löytynyt ketään juuri nyt 😔",
                         "not_username": "Käyttäjänimi puuttuu ❌",
                         "reloaded": "Valikko päivitetty 🔄",
                         "empty": "Ei löydy",
                         "LOVE": "Haluat treffit {name} kanssa",
                         "SEX": "Haluat {name}",
                         "CHAT": "Haluat jutella {name} kanssa",
                         "SKIP": "Ohitit {name}",
                         "delete": "Käyttäjä poistettu ❌",
                         "payment_sent": "Maksu lähetetty ⭐️",
                         "unavailable": "Käyttäjä {name} ei ole juuri nyt käytettävissä 🚫",
                         "incognito" : {
                             True: "Incognito-tila käytössä ✅",
                             False: "Incognito-tila pois päältä 🚫"},
                         },
        "match_menu":{"start": "Täällä voit katsoa:"
                      "\n🔹 Osumat – teidän toiveenne täsmäsivät"
                      "\n🔹 Kokoelma – sait oikeuden jutella näiden ihmisten kanssa"
                      "\n🔹 Toisten reaktiot profiiliisi",
                      "you_want": "Te molemmat haluatte {reaction}",
                      "empty": {"LOVE": "Tänne ilmestyy ihmisiä, jotka haluavat lähteä kanssasi ☕ <b>Treffeille</b>",
                                "SEX": "Tänne ilmestyy ihmisiä, jotka haluavat kanssasi 👩‍❤️‍💋‍👨 <b>Sänkyyn</b>",
                                "CHAT": "Tänne ilmestyy ihmisiä, jotka haluavat 💬 <b>Jutella</b> kanssasi"},
                      "match_empty": "Tänne ilmestyy ihmisiä, joiden kanssa toiveesi täsmäävät"
                                    "\nVoit lähettää heille viestin ✉️",
                      "collection_empty": "Kokoelma on tyhjä"
                                           "\nLisää profiileja kokoelmaan ✨."
                                           "\nVoit kirjoittaa viestin kokoelman henkilöille ✉️"},
        "search_menu":{"start": "🔍 Etsi kumppania",
                       "not_found": "Alueeltasi ei löytynyt ketään 😔"
                       "\nKokeile myöhemmin ☕"},
        "payment": {"incognito":{"label": "Aktivoi Incognito-tila",
                                 "title": "Aktivoi Incognito-tila",
                                "description": "Osta kerran — ja voit kytkeä sen päälle/pois milloin tahansa!"
                                "\nTässä tilassa sinua ei näy haussa, mutta voit itse selata muiden profiileja."},

                    "collection": {"label": "Lisää {target_name} ✨ Kokoelmaan",
                                   "title": "Lisää {target_name} ✨ Kokoelmaan ",
                                   "description": "Kun lisäät ✨ Kokoelmaan, saat pääsyn {target_name} profiiliin ja voit lähettää hänelle viestin" }
        }}


BUTTONS_TEXT = {
    "begin":"Aloita ✅",
    "reload": "Päivitä 🔄",
    "back":"⬅️ Takaisin",
    "next":"Seuraava ➡️",
    "return":"⏮️ Valikkoon",
    "delete": "🗑️ Poista",
    "search_menu": {"start":"🔍 Haku"},
    "pay": "Maksa ⭐️",
    "reaction": {
        "LOVE":"☕ Treffit",
        "SEX":"🔥 Sänky",
        "CHAT": "💬 Jutella",
        "SKIP":"⏩ Ohita"
    },
    "match_menu":{
        "start":"💘 Osumat",
        "match":"💘 Osumat [{match_count}]",
        "collection":"✨ Lista [{collection_count}]",
        "love":"Treffit [{love_count}]",
        "sex":"Sänky [{sex_count}]",
        "chat":"Juttelu [{chat_count}]",
        "add_to_collection":"Lisää {amount} ⭐️",
        "send_message":"✉️ Viesti"
    },
    "gender": {
        "man": "Mies 🧔🏻",
        "woman":"Nainen 👩🏻‍🦰",
        "any":"Muu 👱"
    },
    "gender_search": {
        "man": "Etsin miestä 🧔🏻",
        "woman":"Etsin naista 👩🏻‍🦰",
        "any":"Ei väliä 🧔🏻👩🏻‍🦰👱"
    },
    "incognito":{
        "not_active":"🫥 Incognito",
        "on":"✅ Incognito on",
        "off":"🚫 Incognito off"
    },
    "profile":{
        "edit":"✏ Muokkaa",
        "retry":"🔄 Uudestaan"
    },
    "location":{
        "send":"📍 Lähetä",
        "press":"📍 Paina"
    }
}


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Mies 🧔🏻",
    Gender.WOMAN: "Nainen 👩🏻‍🦰",
    Gender.ANY: "Muu 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Etsin miestä 🧔🏻",
    Gender.WOMAN: "Etsin naista 👩🏻‍🦰",
    Gender.ANY: "Sukupuolella ei ole väliä 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
