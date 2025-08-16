from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Salut, <b>{first_name}</b> !\n"
                        "Prêt(e) pour de nouvelles rencontres ?\n\n"
                        "Pour commencer, il suffit de suivre quelques étapes simples :\n\n"
                        "🔸 Étape 1. En appuyant sur «Commencer l’inscription», tu :"
                        "\n🔹Confirms avoir plus de 18 ans 🪪"
                        '\n🔹Acceptes les <a href="{notion_site}">Conditions d’utilisation</a>'
                        '\n🔹Acceptes la <a href="{notion_site}">Politique de confidentialité</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Étape 2. Envoie ta localisation 🛰️\n\n"
                        "<i>La recherche se fera parmi les personnes de ta ville et de ton pays 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Étape 3. Choisis ton genre ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Étape 4. Indique qui tu recherches ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Étape 5. Envoie ta photo 🤳"
                        "\n<i>De préférence un selfie où ton visage est bien visible</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Étape 6. Parle un peu de toi 📝"
                        "\n<i>Essaie d’écrire brièvement — 2-3 lignes</i>",
                        
                        "username_error": "⚠️ Pour utiliser le bot, tu dois définir un <b>nom d’utilisateur</b> dans Telegram."
                        "\nComment faire :"
                        "\n1️⃣ Ouvre Telegram → Paramètres → Nom d’utilisateur (tg://settings/username)"
                        "\n2️⃣ Choisis un <b>nom d’utilisateur</b> unique"
                        "\n3️⃣ Sauvegarde les changements ✅"
                        "\nEnsuite, reviens dans le bot et appuie sur «Relancer l’inscription»",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Étape 6 non validée"
                        "\nMinimum — {MIN_COUNT_SYMBOLS} caractères"
                        "\nTu as écrit — {text_length} caractères"
                        "\nEssaie d’ajouter quelques infos et renvoie ton texte",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Étape 6 non validée."
                        "\nLimite dépassée : maximum — {MAX_COUNT_SYMBOLS} caractères."
                        "\nTu as écrit — {text_length} caractères."
                        "\nEssaie de raccourcir ton texte et renvoie-le",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nÀ propos : <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Si tu utilises Telegram sur ordinateur, réalise cette étape sur ton téléphone</i>",
                        "waiting": "En attente ...",
                        },
       
        "notifications":{"18year":"Parfait ! Tu as confirmé avoir plus de 18 ans",
                         "gender": "Parfait ! Tu as indiqué : {user_gender}",
                         "gender_search": "Parfait ! Tu recherches : {gender_search}",
                         "not_found": "Pour l’instant, personne n’a été trouvé dans ta région 😔",
                         "not_username": "Nom d’utilisateur manquant ❌",
                         "reloaded": "Menu mis à jour 🔄",
                         "empty": "Aucun résultat",
                         "LOVE": "Tu veux un rendez-vous avec {name}",
                         "SEX": "Tu veux une relation intime avec {name}",
                         "CHAT": "Tu veux discuter avec {name}",
                         "SKIP": "Tu as passé {name}",
                         "delete": "Utilisateur supprimé ❌",
                         "payment_sent": "Paiement envoyé ⭐️",
                         "unavailable": "Le compte de {name} est actuellement indisponible 🚫",
                         "incognito" : {
                             True: "Mode Incognito activé ✅",
                             False: "Mode Incognito désactivé 🚫"},
                         },
        "match_menu":{"start": "Ici, tu peux voir :"
                      "\n🔹 Les correspondances — vos envies coïncident"
                      "\n🔹 La collection — tu as débloqué l’accès à ces personnes"
                      "\n🔹 Les réactions des autres sur ton profil",
                      "you_want": "Vous voulez tous les deux {reaction}",
                      "empty": {"LOVE": "Ici apparaîtront les personnes qui veulent prendre un 🍷 <b>Rendez-vous</b> avec toi",
                                "SEX": "Ici apparaîtront les personnes qui veulent une 👩‍❤️‍💋‍👨 <b>Relation intime</b> avec toi",
                                "CHAT": "Ici apparaîtront les personnes qui veulent 💬 <b>Discuter</b> avec toi"},
                      "match_empty": "Ici apparaîtront les personnes avec qui vos envies coïncident"
                                    "\nTu pourras leur écrire ✉️",
                      "collection_empty": "Ta collection est vide"
                                           "\nAjoute des profils dans ta collection ✨."
                                           "\nTu pourras leur écrire ✉️"},
        "search_menu":{"start": "🔍 Trouver un partenaire",
                       "not_found": "Pour l’instant, personne n’a été trouvé dans ta région 😔"
                       "\nRéessaie plus tard ☕"},
        "payment": {"incognito":{"label": "Activer le mode Incognito",
                                 "title": "Activer le mode Incognito",
                                "description": "Achète-le une fois — et active/désactive quand tu veux !"
                                "\nDans ce mode, tu n’apparais pas dans les recherches, mais tu peux consulter les profils des autres."},

                    "collection": {"label": "Ajouter {target_name} à ✨ la Collection",
                                   "title": "Ajouter {target_name} à ✨ la Collection ",
                                   "description": "En ajoutant à ✨ la Collection, tu auras accès au profil de {target_name} et tu pourras lui écrire"}
        }}


BUTTONS_TEXT = {"begin":"Commencer l’inscription ✅",
                "reload": "Actualiser 🔄",
                "back":"⬅️ Retour",
                "next":"Suivant ➡️",
                "return":"⏮️ Revenir au menu",
                "delete": "🗑️ Supprimer le profil",
                "search_menu": {"start":"🔍 Commencer la recherche"
                                },
                "pay": "Payer avec Telegram Stars ⭐️",
                "reaction": {"LOVE":"🍷 Rendez-vous",
                             "SEX":"🔥 Relation intime",
                             "CHAT": "💬 Discussion",
                             "SKIP":"Passer ⏩"},
                "match_menu":{"start":"💘 Voir les correspondances",
                              "match":"💘 Correspondances [{match_count}]",
                              "collection":"✨ Collection [{collection_count}]",
                              "love":"Rendez-vous [{love_count}]",
                              "sex":"Relations [{sex_count}]",
                              "chat":"Discussions [{chat_count}]",
                              "add_to_collection":"Ajouter à la Collection {amount} ⭐️",
                              "send_message":"✉️ Envoyer un message"},
                "gender": {"man": "Homme 🧔🏻",
                           "woman":"Femme 👩🏻‍🦰",
                           "any":"Autre 👱"},
                "gender_search": {"man": "Je cherche un homme 🧔🏻",
                                  "woman":"Je cherche une femme 👩🏻‍🦰",
                                  "any":"Peu importe le genre 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Devenir Incognito",
                             "on":"✅ Incognito activé",
                             "off":"🚫 Incognito désactivé",
                             },
                "profile":{"edit":"✏ Modifier le profil",
                           "retry":"🔄 Reprendre l’inscription"},
                "location":{"send":"📍 Envoyer la localisation",
                            "press":"📍 Appuie pour envoyer"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Homme 🧔🏻",
    Gender.WOMAN: "Femme 👩🏻‍🦰",
    Gender.ANY: "Autre 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Je cherche un homme 🧔🏻",
    Gender.WOMAN: "Je cherche une femme 👩🏻‍🦰",
    Gender.ANY: "Peu importe le genre 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
