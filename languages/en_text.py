from models import Gender


TEXT = {
    "user_profile": {
        "step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                  "Hi, <b>{first_name}</b>!\n"
                  "Ready to meet new people?\n\n"
                  "To get started, follow these quick steps:\n\n"
                  "🔸 Step 1. By tapping \"Start Registration\" you:"
                  "\n🔹 Confirm that you're 18 or older 🪪"
                  '\n🔹 Accept our <a href="{notion_site}">Terms of Service</a>'
                  '\n🔹 Agree to the <a href="{notion_site}">Privacy Policy</a>',

        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                  "🔸 Step 2. Share your location 🛰️\n\n"
                  "<i>We’ll match you with people in your city and country 📌</i>",

        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                  "🔸 Step 3. Select your gender ⚧️",

        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                  "🔸 Step 4. Who are you looking for? ⚧️",

        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                  "🔸 Step 5. Upload your <b>PHOTO</b> 📎"
                  "\n<i>A selfie where your face is clearly visible is best 🤳</i>",

        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                  "🔸 Step 6. Tell us a bit about yourself 📝"
                  "\n<i>Just 2–3 sentences is enough</i>",

        "username_error": "⚠️ To use this bot, you need to set a <b>username</b> in Telegram."
                          "\nHow to do it:"
                          "\n1️⃣ Open Telegram → Settings → Username (tg://settings/username)"
                          "\n2️⃣ Choose a unique <b>Username</b>"
                          "\n3️⃣ Save your changes ✅"
                          "\nThen come back to the bot and tap \"Restart Registration\"",

        "min_count_symbols_error": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                                   "❌ Step 6 not completed"
                                   "\nMinimum: {MIN_COUNT_SYMBOLS} characters"
                                   "\nYou wrote: {text_length} characters"
                                   "\nPlease add more and try again.",

        "max_count_symbols_error": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                                   "❌ Step 6 not completed"
                                   "\nToo long: maximum {MAX_COUNT_SYMBOLS} characters allowed"
                                   "\nYou wrote: {text_length} characters"
                                   "\nPlease shorten your description and try again.",

        "profile": "🪪 <b>{first_name}</b>"
                   "\n📌 {country_local}, {city_local}"
                   "\n{gender_emoji} {gender}"
                   "\n🔍 Looking for: {gender_search}"
                   "\nAbout me: <i>{about_me}</i>",

        "get_location_message": "<i>If you're using Telegram on a computer, please complete this step on your mobile device</i>",
        "waiting": "Waiting ...",
    },

    "notifications": {
        "18year": "Great! You've confirmed that you're 18+",
        "gender": "Got it! Your gender: {user_gender}",
        "gender_search": "You're looking for: {gender_search}",
        "not_found": "No matches found in your area just yet 😔",
        "not_username": "The user's name is missing ❌",
        "reloaded": "Updated 🔄",
        "empty": "No results found",
        "LOVE": "You're interested in dating {name}",
        "SEX": "You're interested in intimacy with {name}",
        "CHAT": "You want to chat with {name}",
        "SKIP": "You skipped {name}",
        "delete": "User has been removed ❌",
        "payment_sent": "Payment has been sent ⭐️",
        "unavailable": "The account {name} is currently unavailable 🚫",
        "incognito" : {
            True: "Incognito Mode is ON ✅",
            False: "Incognito Mode is OFF 🚫"
    },

    "match_menu": {
        "start": "Here you can see:"
                 "\n🔹 Matches – mutual interest"
                 "\n🔹 Collection – profiles you unlocked"
                 "\n🔹 Reactions – who showed interest in you",
        "you_want": "You both want: {reaction}",
        "empty": {
            "LOVE": "People who want to go on a ☕ <b>Date</b> with you will appear here",
            "SEX": "People who are open to 🔥 <b>Intimacy</b> will appear here",
            "CHAT": "People who want to 💬 <b>Chat</b> with you will appear here"
        },
        "match_empty": "People with matching intentions will show up here"
                       "\nYou’ll be able to message them ✉️",
        "collection_empty": "Your collection is empty"
                            "\nAdd profiles to your collection ✨"
                            "\nYou can message people from your collection ✉️"
    },

    "search_menu": {
        "start": "🔍 Find a Match",
        "not_found": "No matches found in your region 😔"
                     "\nPlease try again later ☕"
    },

    "payment": {
        "incognito": {
            "label": "Activate Incognito Mode",
            "title": "Enable Incognito Mode",
            "description": "One-time purchase — turn it on or off anytime!"
                           "\nIn this mode, others won’t see your profile in search, but you can still view theirs."
        },
        "collection": {
            "label": "Add {target_name} to ✨ Collection",
            "title": "Add {target_name} to ✨ Collection",
            "description": "Once added, you’ll get access to {target_name}'s profile and be able to message them."
        }
    }
}
}

BUTTONS_TEXT = {
    "begin": "Start Registration ✅",
    "reload": "Refresh 🔄",
    "back": "⬅️ Back",
    "next": "Next ➡️",
    "return": "⏮️ Back to Menu",
    "delete": "🗑️ Delete Profile",

    "search_menu": {
        "start": "🔍 Start Searching"
    },

    "pay": "Pay with Telegram Stars ⭐️",

    "reaction": {
        "LOVE": "☕ Dating",
        "SEX": "🔥 Intimacy",
        "CHAT": "💬 Chat",
        "SKIP": "Skip ⏩"
    },

    "match_menu": {
        "start": "💘 View Matches",
        "match": "💘 Matches [{match_count}]",
        "collection": "✨ Collection [{collection_count}]",
        "love": "Dating [{love_count}]",
        "sex": "Intimacy [{sex_count}]",
        "chat": "Chat [{chat_count}]",
        "add_to_collection": "Add to Collection {amount} ⭐️",
        "send_message": "✉️ Send Message"
    },

    "gender": {
        "man": "Man 🧔🏻",
        "woman": "Woman 👧🏻",
        "any": "Other 👱"
    },

    "gender_search": {
        "man": "Looking for a man 🧔🏻",
        "woman": "Looking for a woman 👩🏻‍🦰",
        "any": "Open to any gender 🧔🏻👩🏻‍🦰👱"
    },

    "incognito": {
        "not_active": "🫥 Go Incognito",
        "on": "✅ Incognito Mode: ON",
        "off": "🚫 Incognito Mode: OFF"
    },

    "profile": {
        "edit": "✏ Edit Profile",
        "retry": "🔄 Restart Registration"
    },

    "location": {
        "send": "📍 Send Location",
        "press": "📍 Tap to Send Location"
    }
}


GENDER_LABELS = {
    Gender.MAN: "Man 🧔🏻",
    Gender.WOMAN: "Woman 👩🏻‍🦰",
    Gender.ANY: "Any 👱",
    }


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Looking for a man 🧔🏻",
    Gender.WOMAN: "Looking for a woman 👩🏻‍🦰",
    Gender.ANY: "Open to any gender 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}