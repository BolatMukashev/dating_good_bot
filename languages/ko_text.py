from models import Gender


TEXT = {"user_profile":{
                        "step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "안녕하세요, <b>{first_name}</b>님!\n"
                        "새로운 인연을 만나볼 준비되셨나요? 💫\n\n"
                        "시작하려면 몇 가지 간단한 단계를 따라주세요:\n\n"
                        "🔸 1단계. «등록 시작» 버튼을 누르면:"
                        "\n🔹 만 18세 이상임을 확인합니다 🪪"
                        '\n🔹 <a href="{notion_site}">이용 약관</a>에 동의합니다'
                        '\n🔹 <a href="{notion_site}">개인정보 처리방침</a>에 동의합니다',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 2단계. 현재 위치를 보내주세요 🛰️\n\n"
                        "<i>동일한 도시와 국가의 사람들과 매칭됩니다 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 3단계. 성별을 선택하세요 ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 4단계. 찾고 있는 상대를 선택하세요 ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 5단계. 사진을 올려주세요 🤳"
                        "\n<i>얼굴이 잘 보이는 셀카가 가장 좋아요</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 6단계. 자기소개를 작성해주세요 📝"
                        "\n<i>짧게 2~3줄 정도면 충분합니다</i>",
                        
                        "username_error": "⚠️ 이 봇을 사용하려면 <b>사용자 이름(username)</b>을 설정해야 합니다."
                        "\n설정 방법:"
                        "\n1️⃣ 텔레그램 → 설정 → 사용자 이름 (tg://settings/username)"
                        "\n2️⃣ 고유한 <b>사용자 이름</b> 입력"
                        "\n3️⃣ 저장 후 ✅"
                        "\n이후 봇으로 돌아와 «등록 다시하기»를 눌러주세요",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6단계 미완료"
                        "\n최소 {MIN_COUNT_SYMBOLS}자 이상 작성해야 합니다."
                        "\n현재 — {text_length}자"
                        "\n조금 더 작성 후 다시 보내주세요",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ 6단계 미완료"
                        "\n최대 {MAX_COUNT_SYMBOLS}자를 초과했습니다."
                        "\n현재 — {text_length}자"
                        "\n내용을 줄이고 다시 보내주세요",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\n자기소개: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>PC에서 텔레그램을 사용 중이라면, 이 단계는 모바일에서 진행해주세요</i>",
                        "waiting": "잠시만 기다려주세요 ...",
                        },
       
        "notifications":{"18year":"좋습니다! 만 18세 이상임을 확인하셨습니다 ✅",
                         "gender": "선택한 성별: {user_gender}",
                         "gender_search": "찾는 상대: {gender_search}",
                         "not_found": "아직은 근처에서 아무도 발견되지 않았습니다 😔",
                         "not_username": "사용자 이름이 없습니다 ❌",
                         "reloaded": "메뉴가 새로고침되었습니다 🔄",
                         "empty": "검색 결과 없음",
                         "LOVE": "{name}님과 데이트하고 싶습니다 ☕",
                         "SEX": "{name}님과 함께하고 싶습니다 🔥",
                         "CHAT": "{name}님과 대화하고 싶습니다 💬",
                         "SKIP": "{name}님을 건너뜀 ⏩",
                         "delete": "사용자가 삭제되었습니다 ❌",
                         "payment_sent": "결제가 완료되었습니다 ⭐️",
                         "unavailable": "{name}님의 계정을 사용할 수 없습니다 🚫",
                         "incognito" : {
                             True: "익명 모드가 켜졌습니다 ✅",
                             False: "익명 모드가 꺼졌습니다 🚫"},
                         },
        "match_menu":{"start": "여기서 확인할 수 있습니다:"
                      "\n🔹 매칭 – 서로의 관심사가 일치"
                      "\n🔹 보관함 – 대화할 수 있는 사람들"
                      "\n🔹 다른 사람이 내 프로필에 보인 반응",
                      "you_want": "서로 {reaction} 원합니다 💘",
                      "empty": {"LOVE": "☕ <b>데이트</b>를 원한 사람들이 여기에 표시됩니다",
                                "SEX": "👩‍❤️‍💋‍👨 <b>관계</b>를 원하는 사람들이 여기에 표시됩니다",
                                "CHAT": "💬 <b>대화</b>를 원하는 사람들이 여기에 표시됩니다"},
                      "match_empty": "아직 매칭된 사람이 없습니다."
                                    "\n매칭되면 메시지를 보낼 수 있어요 ✉️",
                      "collection_empty": "보관함이 비어있습니다."
                                           "\n✨ 마음에 드는 프로필을 추가해보세요."
                                           "\n보관함의 사람들에게는 메시지를 보낼 수 있습니다 ✉️"},
        "search_menu":{"start": "🔍 파트너 찾기",
                       "not_found": "근처에 아직 아무도 없습니다 😔"
                       "\n조금 후에 다시 시도해보세요 ☕"},
        "payment": {"incognito":{"label": "익명 모드 활성화",
                                 "title": "익명 모드 활성화",
                                "description": "한 번만 결제하면 언제든 켜고 끌 수 있습니다!"
                                "\n이 모드에서는 검색에 표시되지 않지만, 다른 사람들의 프로필은 볼 수 있습니다."},

                    "collection": {"label": "{target_name}님을 ✨ 보관함에 추가",
                                   "title": "{target_name}님을 ✨ 보관함에 추가",
                                   "description": "보관함에 추가하면 {target_name}님의 프로필을 확인하고 메시지를 보낼 수 있습니다."}
        }}


BUTTONS_TEXT = {"begin":"등록 시작 ✅",
                "reload": "새로고침 🔄",
                "back":"⬅️ 뒤로",
                "next":"➡️ 다음",
                "return":"⏮️ 메뉴로",
                "delete": "🗑️ 프로필 삭제",
                "search_menu": {"start":"🔍 검색 시작"},
                "pay": "텔레그램 스타즈로 결제 ⭐️",
                "reaction": {"LOVE":"☕ 데이트",
                             "SEX":"🔥 관계",
                             "CHAT": "💬 대화",
                             "SKIP":"⏩ 건너뛰기"},
                "match_menu":{"start":"💘 매칭 보기",
                              "match":"💘 매칭 [{match_count}]",
                              "collection":"✨ 보관함 [{collection_count}]",
                              "love":"데이트 [{love_count}]",
                              "sex":"관계 [{sex_count}]",
                              "chat":"대화 [{chat_count}]",
                              "add_to_collection":"보관함 추가 {amount} ⭐️",
                              "send_message":"✉️ 메시지 보내기"},
                "gender": {"man": "남자 🧔🏻",
                           "woman":"여자 👩🏻‍🦰",
                           "any":"기타 👱"},
                "gender_search": {"man": "남자를 찾습니다 🧔🏻",
                                  "woman":"여자를 찾습니다 👩🏻‍🦰",
                                  "any":"성별 상관 없음 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 익명 모드",
                             "on":"✅ 익명 켜짐",
                             "off":"🚫 익명 꺼짐"},
                "profile":{"edit":"✏ 프로필 수정",
                           "retry":"🔄 등록 다시하기"},
                "location":{"send":"📍 위치 보내기",
                            "press":"📍 눌러서 보내기"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "남자 🧔🏻",
    Gender.WOMAN: "여자 👩🏻‍🦰",
    Gender.ANY: "기타 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "남자를 찾습니다 🧔🏻",
    Gender.WOMAN: "여자를 찾습니다 👩🏻‍🦰",
    Gender.ANY: "성별 상관 없음 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
