from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "嗨，<b>{first_name}</b>!\n"
                        "準備好認識新朋友了嗎？💫\n\n"
                        "開始之前，需要完成幾個簡單步驟：\n\n"
                        "🔸 步驟 1. 點擊「開始註冊」你將："
                        "\n🔹確認你已滿 18 歲 🪪"
                        '\n🔹同意 <a href="{notion_site}">用戶協議</a>'
                        '\n🔹同意 <a href="{notion_site}">隱私政策</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 步驟 2. 傳送你的位置 🛰️\n\n"
                        "<i>搜索將基於你的城市和國家 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 步驟 3. 選擇你的性別 ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 步驟 4. 選擇你想找的人 ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 步驟 5. 上傳一張照片 🤳"
                        "\n<i>最好是能清楚看到臉的自拍</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 步驟 6. 簡單介紹自己 📝"
                        "\n<i>盡量簡短 — 2-3 行</i>",

                        "username_error": "⚠️ 使用機器人前需要先設定 <b>用戶名</b>。"
                        "\n操作方法："
                        "\n1️⃣ 打開 Telegram → 設定 → 用戶名 (tg://settings/username)"
                        "\n2️⃣ 設定唯一 <b>用戶名</b>"
                        "\n3️⃣ 保存 ✅"
                        "\n然後返回機器人，點擊「重新註冊」",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 步驟 6 未完成"
                        "\n最少需要 {MIN_COUNT_SYMBOLS} 個字元"
                        "\n你輸入了 {text_length} 個字元"
                        "\n請補充介紹後再發送一次",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 步驟 6 未完成"
                        "\n超出字元限制：最多 {MAX_COUNT_SYMBOLS} 個"
                        "\n你輸入了 {text_length} 個字元"
                        "\n請精簡後再發送",

                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\n簡介: <i>{about_me}</i>",

                        "get_location_message": "<i>如果在電腦上使用 Telegram，請在手機上完成此步驟</i>",
                        "waiting": "等待中 ...",
                        },

        "notifications":{"18year":"太棒了！你已確認滿 18 歲 ✅",
                         "gender": "已選擇: {user_gender}",
                         "gender_search": "已選擇: {gender_search}",
                         "not_found": "暫時沒有找到合適的人 😔",
                         "not_username": "未設定用戶名 ❌",
                         "reloaded": "選單已刷新 🔄",
                         "empty": "暫無內容",
                         "LOVE": "你想和 {name} 約會 ☕",
                         "SEX": "你想和 {name} 親密 🔥",
                         "CHAT": "你想和 {name} 聊天 💬",
                         "SKIP": "你跳過了 {name} ⏩",
                         "delete": "使用者已刪除 ❌",
                         "payment_sent": "付款成功 ⭐️",
                         "unavailable": "{name} 帳號暫不可用 🚫",
                         "incognito" : {
                             True: "隱身模式已開啟 ✅",
                             False: "隱身模式已關閉 🚫"},
                         },

        "match_menu":{"start": "這裡你可以查看："
                      "\n🔹 匹配 - 彼此心意相同"
                      "\n🔹 收藏 - 解鎖與他們聊天權限"
                      "\n🔹 別人對你資料的反應",
                      "you_want": "你們都選擇了 {reaction}",
                      "empty": {"LOVE": "這裡會顯示想和你 ☕ <b>約會</b> 的人",
                                "SEX": "這裡會顯示想和你 👩‍❤️‍💋‍👨 <b>親密</b> 的人",
                                "CHAT": "這裡會顯示想和你 💬 <b>聊天</b> 的人"},
                      "match_empty": "這裡會顯示匹配成功的人"
                                    "\n你可以發送訊息 ✉️",
                      "collection_empty": "收藏夾為空"
                                           "\n快把心動的資料加入 ✨"
                                           "\n可以直接發訊息 ✉️"},
        "search_menu":{"start": "🔍 開始尋找",
                       "not_found": "暫時沒有找到合適的人 😔"
                       "\n稍後再試 ☕"},
        "payment": {"incognito":{"label": "開啟隱身模式",
                                 "title": "隱身模式",
                                "description": "一次購買，隨時切換！"
                                "\n開啟後，你不會出現在搜索中，但可以自由查看別人資料。"},
                    "collection": {"label": "加入 {target_name} 到 ✨ 收藏",
                                   "title": "將 {target_name} 加入 ✨ 收藏",
                                   "description": "加入後，你可以解鎖 {target_name} 的資料，並可直接發訊息"}}
        }


BUTTONS_TEXT = {"begin":"開始註冊 ✅",
                "reload": "刷新 🔄",
                "back":"⬅️ 返回",
                "next":"➡️ 下一步",
                "return":"⏮️ 回選單",
                "delete": "🗑️ 刪除資料",
                "search_menu": {"start":"🔍 搜尋"},
                "pay": "用 Telegram Stars 支付 ⭐️",
                "reaction": {"LOVE":"☕ 約會",
                             "SEX":"🔥 親密",
                             "CHAT":"💬 聊天",
                             "SKIP":"⏩ 跳過"},
                "match_menu":{"start":"💘 查看匹配",
                              "match":"💘 匹配 [{match_count}]",
                              "collection":"✨ 收藏 [{collection_count}]",
                              "love":"約會 [{love_count}]",
                              "sex":"親密 [{sex_count}]",
                              "chat":"聊天 [{chat_count}]",
                              "add_to_collection":"加入收藏 {amount} ⭐️",
                              "send_message":"✉️ 發訊息"},
                "gender": {"man": "男生 🧔🏻",
                           "woman":"女生 👩🏻‍🦰",
                           "any":"其他 👱"},
                "gender_search": {"man": "找男生 🧔🏻",
                                  "woman":"找女生 👩🏻‍🦰",
                                  "any":"不限 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 開啟隱身",
                             "on":"✅ 已隱身",
                             "off":"🚫 已關閉"},
                "profile":{"edit":"✏ 編輯資料",
                           "retry":"🔄 重新註冊"},
                "location":{"send":"📍 傳送位置",
                            "press":"📍 點擊傳送"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "男生 🧔🏻",
    Gender.WOMAN: "女生 👩🏻‍🦰",
    Gender.ANY: "其他 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "找男生 🧔🏻",
    Gender.WOMAN: "找女生 👩🏻‍🦰",
    Gender.ANY: "不限 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
