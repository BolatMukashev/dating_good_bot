from models import Gender


TEXT = {"user_profile":{
    "step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
              "こんにちは、<b>{first_name}</b>さん！\n"
              "新しい出会いの準備はできましたか？\n\n"
              "スタートするには、いくつかの簡単なステップを進めましょう:\n\n"
              "🔸 ステップ 1. 「登録を開始」を押すと、あなたは次に同意します:"
              "\n🔹18歳以上であること 🪪"
              '\n🔹<a href="{notion_site}">利用規約</a>に同意すること'
              '\n🔹<a href="{notion_site}">プライバシーポリシー</a>に同意すること',

    "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
              "🔸 ステップ 2. 現在地を送信してください 🛰️\n\n"
              "<i>同じ都市や国の人とマッチングされます 📌</i>",

    "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
              "🔸 ステップ 3. 性別を選んでください ⚧️",

    "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
              "🔸 ステップ 4. 探している相手を選んでください ⚧️",

    "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
              "🔸 ステップ 5. 写真を送ってください 🤳"
              "\n<i>顔がはっきり見えるセルフィーがおすすめです</i>",

    "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
              "🔸 ステップ 6. 自己紹介を書いてください 📝"
              "\n<i>2〜3行で簡潔にまとめてください</i>",

    "username_error": "⚠️ このボットを利用するには <b>ユーザー名</b> を設定してください。"
                      "\n設定方法:"
                      "\n1️⃣ Telegram → 設定 → ユーザー名 (tg://settings/username)"
                      "\n2️⃣ ユニークな<b>ユーザー名</b>を作成"
                      "\n3️⃣ 保存 ✅"
                      "\n設定後、「再登録」を押してください。",

    "min_count_symbols_error": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                               "❌ ステップ 6 未完了"
                               "\n最小 — {MIN_COUNT_SYMBOLS} 文字"
                               "\nあなたの入力 — {text_length} 文字"
                               "\n内容を追加してもう一度送信してください。",

    "max_count_symbols_error": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                               "❌ ステップ 6 未完了"
                               "\n上限を超えています: 最大 — {MAX_COUNT_SYMBOLS} 文字"
                               "\nあなたの入力 — {text_length} 文字"
                               "\n短くして再度送信してください。",

    "profile": "🪪 <b>{first_name}</b>"
               "\n📌 {country_local}, {city_local}"
               "\n{gender_emoji} {gender}"
               "\n🔍 {gender_search}"
               "\n自己紹介: <i>{about_me}</i>",

    "get_location_message": "<i>PC版Telegramを利用している場合、このステップはスマホで行ってください</i>",
    "waiting": "待機中 ..."
    },

    "notifications":{
        "18year": "確認しました！ あなたは18歳以上です ✅",
        "gender": "性別を登録しました: {user_gender}",
        "gender_search": "探している相手: {gender_search}",
        "not_found": "現在、あなたの地域では見つかりませんでした 😔",
        "not_username": "ユーザー名がありません ❌",
        "reloaded": "メニューを更新しました 🔄",
        "empty": "見つかりませんでした",
        "LOVE": "{name}とデートしたい 💕",
        "SEX": "{name}と親密になりたい 🔥",
        "CHAT": "{name}とチャットしたい 💬",
        "SKIP": "{name}をスキップしました ⏩",
        "delete": "ユーザーが削除されました ❌",
        "payment_sent": "支払いが送信されました ⭐️",
        "unavailable": "{name} は現在利用できません 🚫",
        "incognito": {
            True: "シークレットモード ON ✅",
            False: "シークレットモード OFF 🚫"}
    },

    "match_menu":{
        "start": "ここでは次が見られます:"
                 "\n🔹 マッチ — お互いの希望が一致"
                 "\n🔹 コレクション — あなたが解放したプロフィール"
                 "\n🔹 他の人からのリアクション",
        "you_want": "あなたと相手の希望が一致: {reaction}",
        "empty": {
            "LOVE": "ここには☕ <b>デート</b>を希望している人が表示されます",
            "SEX": "ここには👩‍❤️‍💋‍👨 <b>親密な関係</b>を希望している人が表示されます",
            "CHAT": "ここには💬 <b>チャット</b>を希望している人が表示されます"},
        "match_empty": "ここには希望が一致した相手が表示されます"
                       "\nメッセージを送ることができます ✉️",
        "collection_empty": "コレクションは空です"
                            "\nプロフィールを追加しましょう ✨"
                            "\nコレクション内の人にはメッセージを送れます ✉️"},
    
    "search_menu":{
        "start": "🔍 パートナーを探す",
        "not_found": "現在、あなたの地域では見つかりませんでした 😔"
                     "\n後でもう一度試してください ☕"},
    
    "payment":{
        "incognito":{
            "label": "シークレットモードを有効化",
            "title": "シークレットモードを有効化",
            "description": "一度購入すれば自由にオン/オフ切り替え可能！"
                           "\n検索には表示されませんが、自分は他人のプロフィールを閲覧できます。"},
        
        "collection":{
            "label": "{target_name} を ✨ コレクションに追加",
            "title": "{target_name} を ✨ コレクションに追加",
            "description": "追加すると {target_name} のプロフィールにアクセスでき、メッセージも送れます。"}
    }}


BUTTONS_TEXT = {
    "begin":"登録開始 ✅",
    "reload": "更新 🔄",
    "back":"⬅️ 戻る",
    "next":"➡️ 次へ",
    "return":"⏮️ メニューに戻る",
    "delete": "🗑️ プロフィール削除",
    "search_menu": {"start":"🔍 探す"},
    "pay": "Telegram Stars で支払う ⭐️",
    "reaction": {
        "LOVE":"☕ デート",
        "SEX":"🔥 親密",
        "CHAT":"💬 チャット",
        "SKIP":"⏩ スキップ"},
    "match_menu":{
        "start":"💘 マッチを見る",
        "match":"💘 マッチ [{match_count}]",
        "collection":"✨ コレクション [{collection_count}]",
        "love":"デート [{love_count}]",
        "sex":"親密 [{sex_count}]",
        "chat":"チャット [{chat_count}]",
        "add_to_collection":"{amount} ⭐️で追加",
        "send_message":"✉️ メッセージ"},
    "gender": {
        "man": "男性 🧔🏻",
        "woman":"女性 👩🏻‍🦰",
        "any":"その他 👱"},
    "gender_search": {
        "man": "男性を探す 🧔🏻",
        "woman":"女性を探す 👩🏻‍🦰",
        "any":"性別は問わない 🧔🏻👩🏻‍🦰👱"},
    "incognito":{
        "not_active":"🫥 シークレット",
        "on":"✅ シークレットON",
        "off":"🚫 シークレットOFF"},
    "profile":{
        "edit":"✏ プロフィール編集",
        "retry":"🔄 再登録"},
    "location":{
        "send":"📍 位置情報を送信",
        "press":"📍 タップして送信"}
}


GENDER_LABELS = {
    Gender.MAN: "男性 🧔🏻",
    Gender.WOMAN: "女性 👩🏻‍🦰",
    Gender.ANY: "その他 👱",
}

GENDER_SEARCH_LABELS = {
    Gender.MAN: "男性を探す 🧔🏻",
    Gender.WOMAN: "女性を探す 👩🏻‍🦰",
    Gender.ANY: "性別は問わない 🧔🏻👩🏻‍🦰👱",
}

GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
