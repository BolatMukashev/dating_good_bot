from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "嗨，<b>{first_name}</b>!\n"
                        "准备好认识新朋友了吗？💫\n\n"
                        "开始之前，需要完成几个简单的步骤：\n\n"
                        "🔸 步骤 1. 点击「开始注册」你将："
                        "\n🔹确认你已满 18 岁 🪪"
                        '\n🔹接受 <a href="{notion_site}">用户协议</a>'
                        '\n🔹同意 <a href="{notion_site}">隐私政策</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 步骤 2. 发送你的位置 🛰️\n\n"
                        "<i>搜索会在你的城市和国家范围内进行 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 步骤 3. 选择你的性别 ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 步骤 4. 选择你想找的人 ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 步骤 5. 发送一张照片 🤳"
                        "\n<i>最好是能清楚看到脸的自拍</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 步骤 6. 简单介绍一下自己 📝"
                        "\n<i>尽量简短 — 2-3 行</i>",
                        
                        "username_error": "⚠️ 使用机器人需要先设置 <b>用户名</b>。"
                        "\n操作方法："
                        "\n1️⃣ 打开 Telegram → 设置 → 用户名 (tg://settings/username)"
                        "\n2️⃣ 设置一个唯一的 <b>用户名</b>"
                        "\n3️⃣ 保存 ✅"
                        "\n然后返回机器人，点击“重新注册”",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 步骤 6 未完成"
                        "\n最少需要 {MIN_COUNT_SYMBOLS} 个字符"
                        "\n你现在只有 {text_length} 个"
                        "\n请补充介绍后再发送一次",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 步骤 6 未完成"
                        "\n已超出限制：最多 {MAX_COUNT_SYMBOLS} 个字符"
                        "\n你现在有 {text_length} 个"
                        "\n请精简后再发送一次",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\n个人简介: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>如果你在电脑上使用 Telegram，请在手机上完成此步骤</i>",
                        "waiting": "等待中 ...",
                        },
       
        "notifications":{"18year":"很好！你确认已满 18 岁 ✅",
                         "gender": "已选择: {user_gender}",
                         "gender_search": "已选择: {gender_search}",
                         "not_found": "暂时没有找到合适的人 😔",
                         "not_username": "未设置用户名 ❌",
                         "reloaded": "菜单已刷新 🔄",
                         "empty": "暂无内容",
                         "LOVE": "你想和 {name} 约会 ☕",
                         "SEX": "你想和 {name} 亲密 🔥",
                         "CHAT": "你想和 {name} 聊天 💬",
                         "SKIP": "你跳过了 {name} ⏩",
                         "delete": "用户已删除 ❌",
                         "payment_sent": "支付成功 ⭐️",
                         "unavailable": "{name} 账号暂不可用 🚫",
                         "incognito" : {
                             True: "隐身模式已开启 ✅",
                             False: "隐身模式已关闭 🚫"},
                         },
        "match_menu":{"start": "在这里你可以查看："
                      "\n🔹 匹配 - 彼此心意相同"
                      "\n🔹 收藏 - 你已解锁与他们的聊天权限"
                      "\n🔹 别人对你资料的反应",
                      "you_want": "你们都选择了 {reaction}",
                      "empty": {"LOVE": "这里会出现想和你 ☕ <b>约会</b> 的人",
                                "SEX": "这里会出现想和你 👩‍❤️‍💋‍👨 <b>亲密</b> 的人",
                                "CHAT": "这里会出现想和你 💬 <b>聊天</b> 的人"},
                      "match_empty": "这里会出现和你心意相同的人"
                                    "\n你可以主动发消息 ✉️",
                      "collection_empty": "收藏夹是空的"
                                           "\n快把心动的资料加进来吧 ✨"
                                           "\n你可以主动发消息 ✉️"},
        "search_menu":{"start": "🔍 开始寻找",
                       "not_found": "暂时没有找到合适的人 😔"
                       "\n稍后再试 ☕"},
        "payment": {"incognito":{"label": "开启隐身模式",
                                 "title": "隐身模式",
                                "description": "一次购买，随时切换！"
                                "\n开启后，你不会出现在搜索中，但你可以自由查看别人资料。"},
                    "collection": {"label": "加入 {target_name} 到 ✨ 收藏",
                                   "title": "将 {target_name} 加入 ✨ 收藏 ",
                                   "description": "加入收藏后，你可以解锁 {target_name} 的资料，并能直接发消息"}}
        }


BUTTONS_TEXT = {"begin":"开始注册 ✅",
                "reload": "刷新 🔄",
                "back":"⬅️ 返回",
                "next":"➡️ 下一步",
                "return":"⏮️ 回菜单",
                "delete": "🗑️ 删除资料",
                "search_menu": {"start":"🔍 开始寻找"},
                "pay": "用 Telegram Stars 支付 ⭐️",
                "reaction": {"LOVE":"☕ 约会",
                             "SEX":"🔥 亲密",
                             "CHAT":"💬 聊天",
                             "SKIP":"⏩ 跳过"},
                "match_menu":{"start":"💘 查看匹配",
                              "match":"💘 匹配 [{match_count}]",
                              "collection":"✨ 收藏 [{collection_count}]",
                              "love":"约会 [{love_count}]",
                              "sex":"亲密 [{sex_count}]",
                              "chat":"聊天 [{chat_count}]",
                              "add_to_collection":"加到收藏 {amount} ⭐️",
                              "send_message":"✉️ 发消息"},
                "gender": {"man": "男生 🧔🏻",
                           "woman":"女生 👩🏻‍🦰",
                           "any":"其他 👱"},
                "gender_search": {"man": "找男生 🧔🏻",
                                  "woman":"找女生 👩🏻‍🦰",
                                  "any":"不限 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 开启隐身",
                             "on":"✅ 已隐身",
                             "off":"🚫 已关闭"},
                "profile":{"edit":"✏ 编辑资料",
                           "retry":"🔄 重新注册"},
                "location":{"send":"📍 发送位置",
                            "press":"📍 点击发送"}
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
