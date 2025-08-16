from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "שלום, <b>{first_name}</b>!\n"
                        "מוכן להכיר אנשים חדשים?\n\n"
                        "כדי להתחיל צריך לבצע כמה שלבים פשוטים:\n\n"
                        "🔸 שלב 1. בלחיצה על «התחל הרשמה» אתה:"
                        "\n🔹מאשר שמלאו לך 18 🪪"
                        '\n🔹מקבל את <a href="{notion_site}">תנאי השימוש</a>'
                        '\n🔹מסכים ל<a href="{notion_site}">מדיניות הפרטיות</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 שלב 2. שלח את המיקום שלך 🛰️\n\n"
                        "<i>החיפוש יתבצע בין אנשים בעיר ובמדינה שלך 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 שלב 3. בחר את המגדר שלך ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 שלב 4. ציין את מי אתה מחפש ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 שלב 5. שלח תמונה שלך 🤳"
                        "\n<i>מומלץ סלפי שבו הפנים נראות בבירור</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 שלב 6. ספר קצת על עצמך 📝"
                        "\n<i>נסה לכתוב בקצרה — 2-3 שורות</i>",
                        
                        "username_error": "⚠️ כדי להשתמש בבוט, עליך להגדיר <b>שם משתמש</b> בטלגרם."
                        "\nאיך לעשות זאת:"
                        "\n1️⃣ פתח את Telegram → הגדרות → שם משתמש (tg://settings/username)"
                        "\n2️⃣ המצא <b>שם משתמש</b> ייחודי"
                        "\n3️⃣ שמור את השינויים ✅"
                        "\nלאחר מכן חזור לבוט ולחץ \"חזור להרשמה\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ שלב 6 לא הושלם"
                        "\nמינימום — {MIN_COUNT_SYMBOLS} תווים"
                        "\nיש לך - {text_length} תווים"
                        "\nנסה להוסיף מידע ושלח שוב",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ שלב 6 לא הושלם."
                        "\nחריגה מהגבול: מקסימום — {MAX_COUNT_SYMBOLS} תווים."
                        "\nיש לך — {text_length} תווים."
                        "\nנסה לקצר את הטקסט ושלח שוב",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nעל עצמי: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>אם אתה משתמש בטלגרם במחשב, בצע שלב זה במכשיר נייד</i>",
                        "waiting": "ממתין ...",
                        },
       
        "notifications":{"18year":"מעולה! אישרת שמלאו לך 18",
                         "gender": "מעולה! ציינת: {user_gender}",
                         "gender_search": "מעולה! ציינת: {gender_search}",
                         "not_found": "כרגע לא נמצאו אנשים באזור שלך 😔",
                         "not_username": "אין שם משתמש ❌",
                         "reloaded": "התפריט עודכן 🔄",
                         "empty": "לא נמצא",
                         "LOVE": "אתה רוצה לצאת לדייט עם {name}",
                         "SEX": "אתה רוצה {name}",
                         "CHAT": "אתה רוצה לשוחח עם {name}",
                         "SKIP": "דילגת על {name}",
                         "delete": "המשתמש נמחק ❌",
                         "payment_sent": "התשלום נשלח ⭐️",
                         "unavailable": "החשבון {name} אינו זמין כעת 🚫",
                         "incognito" : {
                             True: "מצב אינקוגניטו הופעל ✅",
                             False: "מצב אינקוגניטו כבוי 🚫"},
                         },
        "match_menu":{"start": "כאן תוכל לראות:"
                      "\n🔹 התאמות - הרצונות שלכם זהים"
                      "\n🔹 אוסף - אנשים שפתחת אליהם גישה"
                      "\n🔹 תגובות של אחרים לפרופיל שלך",
                      "you_want": "שניכם רוצים {reaction}",
                      "empty": {"LOVE": "כאן יופיעו אנשים שרוצים לצאת איתך ל☕ <b>דייט</b>",
                                "SEX": "כאן יופיעו אנשים שרוצים איתך 👩‍❤️‍💋‍👨 <b>יחסים</b>",
                                "CHAT": "כאן יופיעו אנשים שרוצים 💬 <b>שיחה</b> איתך"},
                      "match_empty": "כאן יופיעו אנשים שהרצונות שלכם חופפים"
                                    "\nתוכל לשלוח להם הודעה ✉️",
                      "collection_empty": "האוסף ריק"
                                           "\nהוסף פרופילים לאוסף ✨."
                                           "\nלאנשים באוסף אפשר לכתוב ✉️"},
        "search_menu":{"start": "🔍 חפש שותף",
                       "not_found": "כרגע לא נמצאו אנשים באזור שלך 😔"
                       "\nנסה שוב מאוחר יותר ☕"},
        "payment": {"incognito":{"label": "הפעל מצב אינקוגניטו",
                                 "title": "הפעל מצב אינקוגניטו",
                                "description": "רכישה חד-פעמית — תוכל להדליק ולכבות מתי שתרצה!"
                                "\nבמצב זה לא יראו אותך בחיפוש, אבל אתה תוכל לעיין בפרופילים אחרים."},

                    "collection": {"label": "הוסף את {target_name} ל✨ אוסף",
                                   "title": "הוסף את {target_name} ל✨ אוסף ",
                                   "description": "בהוספה ל✨ אוסף, תקבל גישה לפרופיל של {target_name} ותוכל לכתוב לה/לו"}
        }}


BUTTONS_TEXT = {"begin":"התחל ✅",
                "reload": "רענון 🔄",
                "back":"⬅️ חזור",
                "next":"הבא ➡️",
                "return":"⏮️ לתפריט",
                "delete": "🗑️ מחיקה",
                "search_menu": {"start":"🔍 חיפוש"},
                "pay": "תשלום ⭐️",
                "reaction": {"LOVE":"☕ דייט",
                             "SEX":"🔥 יחסים",
                             "CHAT": "💬 צ'אט",
                             "SKIP":"דלג ⏩"},
                "match_menu":{"start":"💘 התאמות",
                              "match":"💘 התאמות [{match_count}]",
                              "collection":"✨ אוסף [{collection_count}]",
                              "love":"דייט [{love_count}]",
                              "sex":"יחסים [{sex_count}]",
                              "chat":"צ'אט [{chat_count}]",
                              "add_to_collection":"הוסף לאוסף {amount} ⭐️",
                              "send_message":"✉️ שלח"},
                "gender": {"man": "בחור 🧔🏻",
                           "woman":"בחורה 👩🏻‍🦰",
                           "any":"אחר 👱"},
                "gender_search": {"man": "מחפש בחור 🧔🏻",
                                  "woman":"מחפש בחורה 👩🏻‍🦰",
                                  "any":"לא משנה 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 אינקוגניטו",
                             "on":"✅ פעיל",
                             "off":"🚫 כבוי"},
                "profile":{"edit":"✏ עריכה",
                           "retry":"🔄 הרשמה מחדש"},
                "location":{"send":"📍 שלח מיקום",
                            "press":"📍 לחץ לשליחה"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "בחור 🧔🏻",
    Gender.WOMAN: "בחורה 👩🏻‍🦰",
    Gender.ANY: "אחר 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "מחפש בחור 🧔🏻",
    Gender.WOMAN: "מחפש בחורה 👩🏻‍🦰",
    Gender.ANY: "המגדר לא משנה 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
