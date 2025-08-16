from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Hey, <b>{first_name}</b>! 👋\n"
                        "Siap cari kenalan baru? 😉\n\n"
                        "Untuk mulai, ada beberapa langkah singkat:\n\n"
                        "🔸 Langkah 1. Dengan menekan «Mulai» kamu:"
                        "\n🔹Konfirmasi umurmu sudah 18+ 🪪"
                        '\n🔹Setuju dengan <a href="{notion_site}">Aturan Pengguna</a>'
                        '\n🔹Setuju dengan <a href="{notion_site}">Kebijakan Privasi</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Langkah 2. Kirim lokasimu 🛰️\n\n"
                        "<i>Agar bisa cari orang di kota & negaramu 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Langkah 3. Pilih gendermu ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Langkah 4. Pilih siapa yang kamu cari ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Langkah 5. Kirim fotomu 🤳"
                        "\n<i>Selfie lebih oke, biar jelas wajahmu</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Langkah 6. Tulis sedikit tentang dirimu 📝"
                        "\n<i>Singkat aja — 2-3 kalimat</i>",
                        
                        "username_error": "⚠️ Untuk pakai bot ini, kamu butuh <b>username</b> di Telegram."
                        "\nCaranya:"
                        "\n1️⃣ Buka Telegram → Pengaturan → Nama Pengguna (tg://settings/username)"
                        "\n2️⃣ Bikin <b>username</b> unik"
                        "\n3️⃣ Simpan ✅"
                        "\nBalik lagi ke bot & klik \"Ulang registrasi\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Langkah 6 belum beres"
                        "\nMinimal — {MIN_COUNT_SYMBOLS} karakter"
                        "\nPunyamu — {text_length} karakter"
                        "\nCoba tambah dikit lalu kirim lagi",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Langkah 6 belum beres."
                        "\nTerlalu panjang: max — {MAX_COUNT_SYMBOLS} karakter."
                        "\nPunyamu — {text_length} karakter."
                        "\nCoba dipendekin lalu kirim lagi",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nTentangku: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Pakai Telegram di PC? Lanjutkan langkah ini via HP</i>",
                        "waiting": "Loading ...",
                        },
       
        "notifications":{"18year":"Mantap! Umurmu udah 18+ ✅",
                         "gender": "Oke! Kamu pilih: {user_gender}",
                         "gender_search": "Oke! Kamu cari: {gender_search}",
                         "not_found": "Belum ada yang match di daerahmu 😔",
                         "not_username": "Belum ada username ❌",
                         "reloaded": "Menu di-refresh 🔄",
                         "empty": "Kosong",
                         "LOVE": "Kamu mau kencan sama {name} ☕",
                         "SEX": "Kamu mau intim sama {name} 🔥",
                         "CHAT": "Kamu mau chat sama {name} 💬",
                         "SKIP": "Kamu skip {name} ⏩",
                         "delete": "Profil dihapus ❌",
                         "payment_sent": "Pembayaran terkirim ⭐️",
                         "unavailable": "Akun {name} lagi nggak aktif 🚫",
                         "incognito" : {
                             True: "Mode Incognito ON ✅",
                             False: "Mode Incognito OFF 🚫"},
                         },
        "match_menu":{"start": "Di sini kamu bisa lihat:"
                      "\n🔹 Match — keinginan kalian sama"
                      "\n🔹 Koleksi — kamu simpan profil buat chat"
                      "\n🔹 Reaksi orang ke profilmu",
                      "you_want": "Kalian berdua pengen {reaction}",
                      "empty": {"LOVE": "Nanti muncul orang yang mau ☕ <b>Kencan</b> sama kamu",
                                "SEX": "Nanti muncul orang yang mau 🔥 <b>Intim</b> sama kamu",
                                "CHAT": "Nanti muncul orang yang mau 💬 <b>Chat</b> sama kamu"},
                      "match_empty": "Nanti muncul orang yang cocok sama kamu"
                                    "\nBisa langsung kirim pesan ✉️",
                      "collection_empty": "Koleksi masih kosong"
                                           "\nTambah profil ke Koleksi ✨."
                                           "\nBisa langsung chat ✉️"},
        "search_menu":{"start": "🔍 Cari pasangan",
                       "not_found": "Belum ada yang match di daerahmu 😔"
                       "\nCoba lagi nanti ☕"},
        "payment": {"incognito":{"label": "Aktifkan Mode Incognito",
                                 "title": "Aktifkan Mode Incognito",
                                "description": "Beli sekali — aktif/nonaktif kapan aja!"
                                "\nMode ini bikin kamu nggak keliatan di pencarian, tapi bisa lihat profil orang lain."},

                    "collection": {"label": "Tambah {target_name} ke ✨ Koleksi",
                                   "title": "Tambah {target_name} ke ✨ Koleksi",
                                   "description": "Kalau tambah ke ✨ Koleksi, kamu bisa akses profil {target_name} & kirim pesan"}
        }}


BUTTONS_TEXT = {"begin":"Mulai ✅",
                "reload": "🔄 Refresh",
                "back":"⬅️ Back",
                "next":"➡️ Next",
                "return":"⏮️ Menu",
                "delete": "🗑️ Hapus",
                "search_menu": {"start":"🔍 Cari"},
                "pay": "Bayar ⭐️",
                "reaction": {"LOVE":"☕ Kencan",
                             "SEX":"🔥 Intim",
                             "CHAT":"💬 Chat",
                             "SKIP":"⏩ Skip"},
                "match_menu":{"start":"💘 Lihat Match",
                              "match":"💘 Match [{match_count}]",
                              "collection":"✨ Koleksi [{collection_count}]",
                              "love":"Kencan [{love_count}]",
                              "sex":"Intim [{sex_count}]",
                              "chat":"Chat [{chat_count}]",
                              "add_to_collection":"Tambah Koleksi {amount} ⭐️",
                              "send_message":"✉️ Chat"},
                "gender": {"man": "Pria 🧔🏻",
                           "woman":"Cewek 👩🏻‍🦰",
                           "any":"Lainnya 👱"},
                "gender_search": {"man": "Cari pria 🧔🏻",
                                  "woman":"Cari cewek 👩🏻‍🦰",
                                  "any":"Bebas 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Jadi Incognito",
                             "on":"✅ Incognito ON",
                             "off":"🚫 Incognito OFF",
                             },
                "profile":{"edit":"✏ Edit",
                           "retry":"🔄 Ulang"},
                "location":{"send":"📍 Kirim",
                            "press":"📍 Tekan"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Pria 🧔🏻",
    Gender.WOMAN: "Cewek 👩🏻‍🦰",
    Gender.ANY: "Lainnya 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Cari pria 🧔🏻",
    Gender.WOMAN: "Cari cewek 👩🏻‍🦰",
    Gender.ANY: "Bebas 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
