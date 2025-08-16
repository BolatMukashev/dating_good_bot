from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Salom, <b>{first_name}</b>!\n"
                        "Yangi tanishuvlarga tayyormisan? 😉\n\n"
                        "Boshlash uchun bir necha oddiy qadamlarni bajarish kerak:\n\n"
                        "🔸 1-qadam. «Ro‘yxatdan o‘tishni boshlash» tugmasini bossang, sen:"
                        "\n🔹18 yoshdan oshganingni tasdiqlaysan 🪪"
                        '\n🔹<a href="{notion_site}">Foydalanuvchi shartlari</a> bilan tanishasan'
                        '\n🔹<a href="{notion_site}">Maxfiylik siyosati</a>ga rozilik berasan',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 2-qadam. Lokatsiyangni yubor 🛰️\n\n"
                        "<i>Qidiruv sening shahar va mamlakating bo‘yicha olib boriladi 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 3-qadam. Jinsingni tanla ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 4-qadam. Qaysi jinsni qidirayotganingni tanla ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 5-qadam. Fotosurat yubor 🤳"
                        "\n<i>Yuzing yaxshi ko‘rinadigan selfi tavsiya qilinadi</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 6-qadam. O‘zing haqida qisqa yoz 📝"
                        "\n<i>2–3 jumlada qisqa yozishga harakat qil</i>",
                        
                        "username_error": "⚠️ Botdan foydalanish uchun Telegram’da <b>username</b> qo‘yish kerak."
                        "\nQanday qilish kerak:"
                        "\n1️⃣ Telegram → Sozlamalar → Username (tg://settings/username)"
                        "\n2️⃣ O‘ziga xos <b>username</b> o‘ylab top"
                        "\n3️⃣ Saqlab qo‘y ✅"
                        "\nShundan keyin botga qaytib «Qayta ro‘yxatdan o‘tish» tugmasini bos",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6-qadam bajarilmadi"
                        "\nMinimal uzunlik — {MIN_COUNT_SYMBOLS} ta belgi"
                        "\nSenda — {text_length} ta belgi"
                        "\nMatnga qo‘shimcha yozib, qaytadan yubor",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6-qadam bajarilmadi."
                        "\nLimitdan oshib ketdi: maksimum — {MAX_COUNT_SYMBOLS} ta belgi."
                        "\nSenda — {text_length} ta belgi."
                        "\nMatnni qisqartirib, qayta yubor",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nO‘zim haqida: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Agar Telegram’dan kompyuterda foydalanayotgan bo‘lsang, bu qadamni telefon orqali bajar</i>",
                        "waiting": "Kutilmoqda ...",
                        },
       
        "notifications":{"18year":"Zo‘r! 18 yoshdan oshganingni tasdiqlading ✅",
                         "gender": "Zo‘r! Jinsing: {user_gender}",
                         "gender_search": "Zo‘r! Qidiruv: {gender_search}",
                         "not_found": "Hozircha sening hududingda hech kim topilmadi 😔",
                         "not_username": "Username o‘rnatilmagan ❌",
                         "reloaded": "Menyu yangilandi 🔄",
                         "empty": "Topilmadi",
                         "LOVE": "Sen {name} bilan uchrashmoqchisan ☕",
                         "SEX": "Sen {name} bilan bo‘lishni xohlaysan 🔥",
                         "CHAT": "Sen {name} bilan gaplashishni xohlaysan 💬",
                         "SKIP": "Sen {name} ni o‘tkazib yubording ⏩",
                         "delete": "Foydalanuvchi o‘chirildi ❌",
                         "payment_sent": "To‘lov yuborildi ⭐️",
                         "unavailable": "{name} hozir mavjud emas 🚫",
                         "incognito" : {
                             True: "Inkognito rejimi yoqildi ✅",
                             False: "Inkognito rejimi o‘chirildi 🚫"},
                         },
        "match_menu":{"start": "Bu yerda ko‘rishing mumkin:"
                      "\n🔹 Mosliklar — istaklaringiz bir xil chiqdi"
                      "\n🔹 Kolleksiya — suhbat uchun ochilganlar"
                      "\n🔹 Boshqalar reaksiyalari — sening anketingga javoblar",
                      "you_want": "Siz ikkalangiz ham {reaction} xohlaysiz",
                      "empty": {"LOVE": "Bu yerda ☕ <b>Uchrashuv</b>ga chiqishni xohlaganlar chiqadi",
                                "SEX": "Bu yerda 👩‍❤️‍💋‍👨 <b>Yaqinlik</b>ni xohlaganlar chiqadi",
                                "CHAT": "Bu yerda 💬 <b>Suhbat</b> qilishni xohlaganlar chiqadi"},
                      "match_empty": "Bu yerda sizning istaklaringiz mos tushgan odamlar chiqadi"
                                    "\nUlarga yozish imkoniyating bo‘ladi ✉️",
                      "collection_empty": "Kolleksiya bo‘sh"
                                           "\nAnketalarni kolleksiyaga qo‘sh ✨."
                                           "\nKolleksiyadagilarga yozishing mumkin ✉️"},
        "search_menu":{"start": "🔍 Hamkor topish",
                       "not_found": "Hozircha hududingda hech kim topilmadi 😔"
                       "\nKeyinroq urinib ko‘r ☕"},
        "payment": {"incognito":{"label": "Inkognito rejimini yoqish",
                                 "title": "Inkognito rejimini yoqish",
                                "description": "Bir marta sotib ol — xohlagan paytda yoqib/o‘chirishing mumkin!"
                                "\nBu rejimda seni qidiruvda ko‘rishmaydi, lekin sen boshqalarni ko‘rishing mumkin."},

                    "collection": {"label": "{target_name} ni ✨ Kolleksiyaga qo‘shish",
                                   "title": "{target_name} ni ✨ Kolleksiyaga qo‘shish",
                                   "description": "✨ Kolleksiyaga qo‘shgandan keyin, sen {target_name} profilini ko‘rib, yozishing mumkin bo‘ladi"}}
        }


BUTTONS_TEXT = {"begin":"Boshlash ✅",
                "reload": "Yangilash 🔄",
                "back":"⬅️ Orqaga",
                "next":"➡️ Oldinga",
                "return":"⏮️ Menyuga qaytish",
                "delete": "🗑️ Anketani o‘chirish",
                "search_menu": {"start":"🔍 Qidirishni boshlash"},
                "pay": "Telegram Stars orqali to‘lash ⭐️",
                "reaction": {"LOVE":"☕ Uchrashuv",
                             "SEX":"🔥 Yaqinlik",
                             "CHAT":"💬 Suhbat",
                             "SKIP":"⏩ O‘tkazib yubor"},
                "match_menu":{"start":"💘 Mosliklarni ko‘rish",
                              "match":"💘 Mosliklar [{match_count}]",
                              "collection":"✨ Kolleksiya [{collection_count}]",
                              "love":"Uchrashuv [{love_count}]",
                              "sex":"Yaqinlik [{sex_count}]",
                              "chat":"Suhbat [{chat_count}]",
                              "add_to_collection":"{amount} ⭐️ evaziga Kolleksiyaga qo‘sh",
                              "send_message":"✉️ Xabar yozish"},
                "gender": {"man":"O‘g‘il 🧔🏻",
                           "woman":"Qiz 👩🏻‍🦰",
                           "any":"Boshqa 👱"},
                "gender_search": {"man":"O‘g‘il qidirmoqdaman 🧔🏻",
                                  "woman":"Qiz qidirmoqdaman 👩🏻‍🦰",
                                  "any":"Farqi yo‘q 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Inkognito bo‘lish",
                             "on":"✅ Inkognito yoqilgan",
                             "off":"🚫 Inkognito o‘chirilgan"},
                "profile":{"edit":"✏️ Anketani tahrirlash",
                           "retry":"🔄 Qayta ro‘yxatdan o‘tish"},
                "location":{"send":"📍 Lokatsiyani yubor",
                            "press":"📍 Yuborish uchun bos"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "O‘g‘il 🧔🏻",
    Gender.WOMAN: "Qiz 👩🏻‍🦰",
    Gender.ANY: "Boshqa 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "O‘g‘il qidirmoqdaman 🧔🏻",
    Gender.WOMAN: "Qiz qidirmoqdaman 👩🏻‍🦰",
    Gender.ANY: "Farqi yo‘q 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
