from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Chào, <b>{first_name}</b>!\n"
                        "Sẵn sàng làm quen mới chưa? 😉\n\n"
                        "Để bắt đầu, chỉ cần vài bước đơn giản:\n\n"
                        "🔸 Bước 1. Khi nhấn «Bắt đầu đăng ký», bạn:"
                        "\n🔹Xác nhận đã đủ 18 tuổi 🪪"
                        '\n🔹Chấp nhận <a href="{notion_site}">Điều khoản sử dụng</a>'
                        '\n🔹Đồng ý với <a href="{notion_site}">Chính sách bảo mật</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Bước 2. Gửi vị trí của bạn 🛰️\n\n"
                        "<i>Tìm kiếm sẽ dựa trên thành phố và quốc gia của bạn 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Bước 3. Chọn giới tính của bạn ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Bước 4. Chọn đối tượng bạn muốn tìm ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Bước 5. Gửi ảnh của bạn 🤳"
                        "\n<i>Tốt nhất là ảnh selfie rõ mặt</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Bước 6. Viết vài dòng giới thiệu về bản thân 📝"
                        "\n<i>Ngắn gọn 2–3 câu thôi nhé</i>",
                        
                        "username_error": "⚠️ Để dùng bot, bạn cần đặt <b>username</b> trong Telegram."
                        "\nCách làm:"
                        "\n1️⃣ Vào Telegram → Cài đặt → Tên người dùng (tg://settings/username)"
                        "\n2️⃣ Tạo tên người dùng <b>duy nhất</b>"
                        "\n3️⃣ Lưu thay đổi ✅"
                        "\nSau đó quay lại bot và nhấn \"Đăng ký lại\"", 

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Bước 6 chưa hoàn thành"
                        "\nTối thiểu — {MIN_COUNT_SYMBOLS} ký tự"
                        "\nBạn nhập — {text_length} ký tự"
                        "\nHãy bổ sung và gửi lại nhé",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Bước 6 chưa hoàn thành"
                        "\nGiới hạn tối đa — {MAX_COUNT_SYMBOLS} ký tự"
                        "\nBạn nhập — {text_length} ký tự"
                        "\nHãy rút gọn và gửi lại nhé",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nGiới thiệu: <i>{about_me}</i>",

                        "get_location_message": "<i>Nếu bạn dùng Telegram trên máy tính, hãy làm bước này trên điện thoại</i>",
                        "waiting": "Đang chờ ...",
                        },
       
        "notifications":{"18year":"Tuyệt! Bạn đã xác nhận đủ 18 tuổi",
                         "gender": "Tuyệt! Bạn chọn: {user_gender}",
                         "gender_search": "Tuyệt! Bạn muốn tìm: {gender_search}",
                         "not_found": "Hiện chưa tìm thấy ai ở khu vực của bạn 😔",
                         "not_username": "Chưa có username ❌",
                         "reloaded": "Đã làm mới menu 🔄",
                         "empty": "Không tìm thấy",
                         "LOVE": "Bạn muốn hẹn hò với {name} ☕",
                         "SEX": "Bạn muốn {name} 🔥",
                         "CHAT": "Bạn muốn trò chuyện với {name} 💬",
                         "SKIP": "Bạn đã bỏ qua {name} ⏩",
                         "delete": "Người dùng đã bị xóa ❌",
                         "payment_sent": "Thanh toán đã gửi ⭐️",
                         "unavailable": "Tài khoản {name} hiện không khả dụng 🚫",
                         "incognito" : {
                             True: "Chế độ Ẩn danh đã bật ✅",
                             False: "Chế độ Ẩn danh đã tắt 🚫"},
                         },
        "match_menu":{"start": "Tại đây bạn có thể xem:"
                      "\n🔹 Ghép đôi - khi mong muốn trùng khớp"
                      "\n🔹 Bộ sưu tập - những người bạn mở trò chuyện"
                      "\n🔹 Phản ứng của người khác với hồ sơ của bạn",
                      "you_want": "Hai bạn đều muốn {reaction}",
                      "empty": {"LOVE": "Ở đây sẽ có những người muốn đi ☕ <b>Hẹn hò</b> với bạn",
                                "SEX": "Ở đây sẽ có những người muốn vào 🔥 <b>Phòng</b> với bạn",
                                "CHAT": "Ở đây sẽ có những người muốn 💬 <b>Trò chuyện</b> với bạn"},
                      "match_empty": "Ở đây sẽ có những người trùng mong muốn với bạn"
                                    "\nBạn có thể nhắn tin ✉️",
                      "collection_empty": "Bộ sưu tập trống"
                                           "\nHãy thêm hồ sơ vào ✨"
                                           "\nBạn có thể nhắn tin cho họ ✉️"},
        "search_menu":{"start": "🔍 Tìm đối tác",
                       "not_found": "Hiện chưa tìm thấy ai ở khu vực của bạn 😔"
                       "\nThử lại sau nhé ☕"},
        "payment": {"incognito":{"label": "Bật chế độ Ẩn danh",
                                 "title": "Bật chế độ Ẩn danh",
                                "description": "Mua một lần — bật/tắt khi bạn muốn!"
                                "\nTrong chế độ này, bạn không hiện trong tìm kiếm, nhưng vẫn xem được hồ sơ người khác."},

                    "collection": {"label": "Thêm {target_name} vào ✨ Bộ sưu tập",
                                   "title": "Thêm {target_name} vào ✨ Bộ sưu tập",
                                   "description": "Khi thêm vào ✨ Bộ sưu tập, bạn có thể mở hồ sơ {target_name} và nhắn tin"}
        }}


BUTTONS_TEXT = {"begin":"Bắt đầu ✅",
                "reload": "Làm mới 🔄",
                "back":"⬅️ Quay lại",
                "next":"➡️ Tiếp",
                "return":"⏮️ Về menu",
                "delete": "🗑️ Xóa hồ sơ",
                "search_menu": {"start":"🔍 Tìm kiếm"},
                "pay": "Thanh toán qua Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Hẹn hò",
                             "SEX":"🔥 Phòng",
                             "CHAT": "💬 Chat",
                             "SKIP":"⏩ Bỏ qua"},
                "match_menu":{"start":"💘 Xem ghép đôi",
                              "match":"💘 Ghép đôi [{match_count}]",
                              "collection":"✨ Bộ sưu tập [{collection_count}]",
                              "love":"Hẹn hò [{love_count}]",
                              "sex":"Phòng [{sex_count}]",
                              "chat":"Chat [{chat_count}]",
                              "add_to_collection":"Thêm vào Bộ sưu tập {amount} ⭐️",
                              "send_message":"✉️ Nhắn tin"},
                "gender": {"man": "Nam 🧔🏻",
                           "woman":"Nữ 👩🏻‍🦰",
                           "any":"Khác 👱"},
                "gender_search": {"man": "Tìm Nam 🧔🏻",
                                  "woman":"Tìm Nữ 👩🏻‍🦰",
                                  "any":"Không quan trọng 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Ẩn danh",
                             "on":"✅ Ẩn danh Bật",
                             "off":"🚫 Ẩn danh Tắt"},
                "profile":{"edit":"✏ Sửa hồ sơ",
                           "retry":"🔄 Đăng ký lại"},
                "location":{"send":"📍 Gửi vị trí",
                            "press":"📍 Nhấn để gửi"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Nam 🧔🏻",
    Gender.WOMAN: "Nữ 👩🏻‍🦰",
    Gender.ANY: "Khác 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Tìm Nam 🧔🏻",
    Gender.WOMAN: "Tìm Nữ 👩🏻‍🦰",
    Gender.ANY: "Không quan trọng 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
