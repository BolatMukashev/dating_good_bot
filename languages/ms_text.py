from models import Gender


TEXT = {"user_profile":{
                        "step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hai, <b>{first_name}</b>!\n"
                        "Ready nak kenal orang baru? 😏\n\n"
                        "Untuk mula, kau kena buat beberapa step mudah:\n\n"
                        "🔸 Step 1. Dengan tekan «Mula daftar» kau:"
                        "\n🔹Confirm dah 18+ 🪪"
                        '\n🔹Setuju dengan <a href="{notion_site}">Perjanjian Pengguna</a>'
                        '\n🔹Setuju dengan <a href="{notion_site}">Dasar Privasi</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Step 2. Hantar lokasi 🛰️\n\n"
                        "<i>Kami cari orang ikut bandar & negara kau 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Step 3. Pilih jantina kau ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Step 4. Nyatakan siapa kau cari ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Step 5. Hantar gambar kau 🤳"
                        "\n<i>Sebaiknya selfie dengan muka jelas</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Step 6. Cerita sikit pasal diri kau 📝"
                        "\n<i>Pendek je cukup — 2-3 baris</i>",
                        
                        "username_error": "⚠️ Untuk guna bot ni, kau kena ada <b>username</b> dalam Telegram."
                        "\nCara buat:"
                        "\n1️⃣ Buka Telegram → Settings → Username (tg://settings/username)"
                        "\n2️⃣ Buat <b>Username unik</b>"
                        "\n3️⃣ Save ✅"
                        "\nLepas tu, balik ke bot & tekan \"Daftar semula\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Step 6 belum siap"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} huruf"
                        "\nKau tulis {text_length} huruf je"
                        "\nTambah sikit lagi & hantar semula",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Step 6 belum siap"
                        "\nLimit lebih: maks — {MAX_COUNT_SYMBOLS} huruf."
                        "\nKau tulis {text_length} huruf."
                        "\nCuba ringkaskan & hantar semula",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nTentang aku: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Kalau kau guna Telegram kat PC, buat step ni kat phone</i>",
                        "waiting": "Tunggu jap ...",
                        },
       
        "notifications":{"18year":"Nice! Kau confirm dah 18+",
                         "gender": "Ok! Kau pilih: {user_gender}",
                         "gender_search": "Ok! Kau cari: {gender_search}",
                         "not_found": "Belum ada orang kat area kau 😔",
                         "not_username": "Username tak ada ❌",
                         "reloaded": "Menu dah refresh 🔄",
                         "empty": "Tak jumpa apa-apa",
                         "LOVE": "Kau nak date dengan {name}",
                         "SEX": "Kau nak {name}",
                         "CHAT": "Kau nak borak dengan {name}",
                         "SKIP": "Kau skip {name}",
                         "delete": "Akaun dah padam ❌",
                         "payment_sent": "Bayaran dah hantar ⭐️",
                         "unavailable": "Akaun {name} tak available 🚫",
                         "incognito" : {
                             True: "Mode Incognito ON ✅",
                             False: "Mode Incognito OFF 🚫"},
                         },
        "match_menu":{"start": "Kat sini kau boleh tengok:"
                      "\n🔹 Match — bila sama-sama nak"
                      "\n🔹 Koleksi — orang yang kau dah unlock chat"
                      "\n🔹 Reaksi orang pada profil kau",
                      "you_want": "Korang dua-dua nak {reaction}",
                      "empty": {"LOVE": "Kat sini nanti muncul orang yang nak ☕ <b>Date</b> dengan kau",
                                "SEX": "Kat sini nanti muncul orang yang nak 👩‍❤️‍💋‍👨 <b>Fun</b> dengan kau",
                                "CHAT": "Kat sini nanti muncul orang yang nak 💬 <b>Borak</b>"},
                      "match_empty": "Kat sini akan muncul orang yang match dengan kau"
                                    "\nBoleh terus chat ✉️",
                      "collection_empty": "Koleksi kosong"
                                           "\nTambah profil ke koleksi ✨."
                                           "\nOrang dari koleksi boleh terus chat ✉️"},
        "search_menu":{"start": "🔍 Cari partner",
                       "not_found": "Belum ada orang kat area kau 😔"
                       "\nCuba lagi nanti ☕"},
        "payment": {"incognito":{"label": "Beli Mode Incognito",
                                 "title": "Aktifkan Mode Incognito",
                                "description": "Beli sekali je — boleh ON/OFF bila-bila!"
                                "\nMode ni buat kau tak muncul dalam carian, tapi kau still boleh tengok profil orang lain."},

                    "collection": {"label": "Tambah {target_name} ke ✨ Koleksi",
                                   "title": "Tambah {target_name} ke ✨ Koleksi",
                                   "description": "Bila tambah ke ✨ Koleksi, kau boleh terus access profil {target_name} & chat"}
        }}


BUTTONS_TEXT = {"begin":"Mula daftar ✅",
                "reload": "Refresh 🔄",
                "back":"⬅️ Balik",
                "next":"➡️ Next",
                "return":"⏮️ Menu utama",
                "delete": "🗑️ Padam profil",
                "search_menu": {"start":"🔍 Cari"},
                "pay": "Bayar dgn Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Date",
                             "SEX":"🔥 Fun",
                             "CHAT": "💬 Borak",
                             "SKIP":"⏩ Skip"},
                "match_menu":{"start":"💘 Tengok Match",
                              "match":"💘 Match [{match_count}]",
                              "collection":"✨ Koleksi [{collection_count}]",
                              "love":"Date [{love_count}]",
                              "sex":"Fun [{sex_count}]",
                              "chat":"Borak [{chat_count}]",
                              "add_to_collection":"Tambah ke Koleksi {amount} ⭐️",
                              "send_message":"✉️ Chat"},
                "gender": {"man": "Lelaki 🧔🏻",
                           "woman":"Perempuan 👩🏻‍🦰",
                           "any":"Lain 👱"},
                "gender_search": {"man": "Cari lelaki 🧔🏻",
                                  "woman":"Cari perempuan 👩🏻‍🦰",
                                  "any":"Tak kisah jantina 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Jadi Incognito",
                             "on":"✅ Incognito ON",
                             "off":"🚫 Incognito OFF"},
                "profile":{"edit":"✏ Edit profil",
                           "retry":"🔄 Daftar semula"},
                "location":{"send":"📍 Hantar lokasi",
                            "press":"📍 Tekan utk hantar"}
                }


GENDER_LABELS = {
    Gender.MAN: "Lelaki 🧔🏻",
    Gender.WOMAN: "Perempuan 👩🏻‍🦰",
    Gender.ANY: "Lain 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Cari lelaki 🧔🏻",
    Gender.WOMAN: "Cari perempuan 👩🏻‍🦰",
    Gender.ANY: "Tak kisah jantina 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
