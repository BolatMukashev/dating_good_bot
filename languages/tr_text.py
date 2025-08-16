from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Merhaba, <b>{first_name}</b>!\n"
                        "Yeni insanlarla tanışmaya hazır mısın? 🤗\n\n"
                        "Başlamak için birkaç basit adım var:\n\n"
                        "🔸 1. Adım. «Kayda başla»ya tıklayarak:"
                        "\n🔹 18 yaşından büyük olduğunu onaylıyorsun 🪪"
                        '\n🔹 <a href="{notion_site}">Kullanıcı Sözleşmesini</a> kabul ediyorsun'
                        '\n🔹 <a href="{notion_site}">Gizlilik Politikasını</a> onaylıyorsun',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 2. Adım. Konumunu paylaş 🛰️\n\n"
                        "<i>Arama, senin şehrin ve ülken içinden yapılacak 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 3. Adım. Cinsiyetini seç ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 4. Adım. Kimi aradığını seç ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 5. Adım. Fotoğrafını gönder 🤳"
                        "\n<i>Tercihen yüzünün net göründüğü bir selfie olsun</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 6. Adım. Kendinden biraz bahset 📝"
                        "\n<i>Kısa yaz: 2-3 satır yeterli</i>",
                        
                        "username_error": "⚠️ Botu kullanmak için Telegram’da <b>kullanıcı adı</b> ayarlaman gerekiyor."
                        "\nNasıl yapılır:"
                        "\n1️⃣ Telegram → Ayarlar → Kullanıcı adı (tg://settings/username)"
                        "\n2️⃣ Kendine benzersiz bir <b>kullanıcı adı</b> seç"
                        "\n3️⃣ Kaydet ✅"
                        "\nSonra bota dönüp \"Kaydı tekrar başlat\"a tıkla",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6. Adım tamamlanmadı"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} karakter"
                        "\nSeninki — {text_length} karakter"
                        "\nBiraz daha ekle ve tekrar gönder",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6. Adım tamamlanmadı"
                        "\nLimit aşıldı: maksimum {MAX_COUNT_SYMBOLS} karakter"
                        "\nSeninki — {text_length} karakter"
                        "\nBiraz kısalt ve tekrar gönder",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nHakkında: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Eğer Telegram’ı bilgisayarda kullanıyorsan, bu adımı telefondan tamamla</i>",
                        "waiting": "Bekleniyor ...",
                        },
       
        "notifications":{"18year":"Harika! 18 yaşından büyük olduğunu onayladın ✅",
                         "gender": "Tamamdır! Cinsiyetin: {user_gender}",
                         "gender_search": "Tamamdır! Aradığın: {gender_search}",
                         "not_found": "Şu an bölgede kimse bulunamadı 😔",
                         "not_username": "Kullanıcı adı yok ❌",
                         "reloaded": "Menü yenilendi 🔄",
                         "empty": "Bulunamadı",
                         "LOVE": "{name} ile buluşmak istiyorsun ☕",
                         "SEX": "{name} ile yakınlaşmak istiyorsun 🔥",
                         "CHAT": "{name} ile sohbet etmek istiyorsun 💬",
                         "SKIP": "{name} atlandı ⏩",
                         "delete": "Profil silindi ❌",
                         "payment_sent": "Ödeme gönderildi ⭐️",
                         "unavailable": "{name} şu anda müsait değil 🚫",
                         "incognito" : {
                             True: "Gizli Mod açıldı ✅",
                             False: "Gizli Mod kapandı 🚫"},
                         },
        "match_menu":{"start": "Buradan görebilirsin:"
                      "\n🔹 Eşleşmeler - ortak istekleriniz"
                      "\n🔹 Koleksiyon - mesaj atabildiğin kişiler"
                      "\n🔹 Senin profiline gelen tepkiler",
                      "you_want": "İkiniz de {reaction} istiyorsunuz",
                      "empty": {"LOVE": "Burada seninle ☕ <b>Buluşmak</b> isteyenler çıkacak",
                                "SEX": "Burada seninle 👩‍❤️‍💋‍👨 <b>Yakınlaşmak</b> isteyenler çıkacak",
                                "CHAT": "Burada seninle 💬 <b>Sohbet</b> isteyenler çıkacak"},
                      "match_empty": "Burada ortak istekleriniz olan kişiler çıkacak"
                                    "\nOnlara mesaj atabilirsin ✉️",
                      "collection_empty": "Koleksiyon boş"
                                           "\nProfil ekle ✨."
                                           "\nKoleksiyondakilere mesaj atabilirsin ✉️"},
        "search_menu":{"start": "🔍 Partner bul",
                       "not_found": "Şu an bölgede kimse bulunamadı 😔"
                       "\nDaha sonra tekrar dene ☕"},
        "payment": {"incognito":{"label": "Gizli Modu Aç",
                                 "title": "Gizli Modu Aç",
                                "description": "Bir kez satın al — istediğin zaman aç/kapat!"
                                "\nBu modda seni kimse göremez ama sen profillere bakabilirsin."},

                    "collection": {"label": "{target_name}’i ✨ Koleksiyona ekle",
                                   "title": "{target_name}’i ✨ Koleksiyona ekle",
                                   "description": "{target_name}’i ✨ Koleksiyonuna ekleyince, profiline erişebilir ve ona mesaj atabilirsin"}}
        }


BUTTONS_TEXT = {"begin":"Kayda başla ✅",
                "reload": "Yenile 🔄",
                "back":"⬅️ Geri",
                "next":"İleri ➡️",
                "return":"⏮️ Menüye dön",
                "delete": "🗑️ Profili sil",
                "search_menu": {"start":"🔍 Ara"},
                "pay": "Telegram Stars ile öde ⭐️",
                "reaction": {"LOVE":"☕ Buluşma",
                             "SEX":"🔥 Yakınlık",
                             "CHAT":"💬 Sohbet",
                             "SKIP":"⏩ Geç"},
                "match_menu":{"start":"💘 Eşleşmeler",
                              "match":"💘 Eşleşmeler [{match_count}]",
                              "collection":"✨ Koleksiyon [{collection_count}]",
                              "love":"Buluşma [{love_count}]",
                              "sex":"Yakınlık [{sex_count}]",
                              "chat":"Sohbet [{chat_count}]",
                              "add_to_collection":"Koleksiyona ekle {amount} ⭐️",
                              "send_message":"✉️ Mesaj gönder"},
                "gender": {"man": "Erkek 🧔🏻",
                           "woman":"Kadın 👩🏻‍🦰",
                           "any":"Diğer 👱"},
                "gender_search": {"man": "Erkek arıyorum 🧔🏻",
                                  "woman":"Kadın arıyorum 👩🏻‍🦰",
                                  "any":"Farketmez 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Gizli ol",
                             "on":"✅ Gizli Mod açık",
                             "off":"🚫 Gizli Mod kapalı"},
                "profile":{"edit":"✏ Profili düzenle",
                           "retry":"🔄 Kaydı tekrar başlat"},
                "location":{"send":"📍 Konum gönder",
                            "press":"📍 Göndermek için tıkla"}}


GENDER_LABELS = {
    Gender.MAN: "Erkek 🧔🏻",
    Gender.WOMAN: "Kadın 👩🏻‍🦰",
    Gender.ANY: "Diğer 👱",
}

GENDER_SEARCH_LABELS = {
    Gender.MAN: "Erkek arıyorum 🧔🏻",
    Gender.WOMAN: "Kadın arıyorum 👩🏻‍🦰",
    Gender.ANY: "Farketmez 🧔🏻👩🏻‍🦰👱",
}

GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
