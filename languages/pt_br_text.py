from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Oi, <b>{first_name}</b>!\n"
                        "Pronto(a) para conhecer gente nova?\n\n"
                        "Pra começar, é só seguir alguns passos simples:\n\n"
                        "🔸 Passo 1. Ao clicar em «Começar cadastro», você:"
                        "\n🔹Confirma que tem 18 anos ou mais 🪪"
                        '\n🔹Aceita os <a href="{notion_site}">Termos de Uso</a>'
                        '\n🔹Concorda com a <a href="{notion_site}">Política de Privacidade</a>',

                        "step_2": "🟢 🔘 ⚪ ⚪ ⚪ ⚪\n\n"
                        "🔸 Passo 2. Envie sua localização 🛰️\n\n"
                        "<i>A busca será feita entre pessoas da sua cidade e país 📌</i>",

                        "step_3": "🟢 🟢 🔘 ⚪ ⚪ ⚪\n\n"
                        "🔸 Passo 3. Escolha seu gênero ⚧️",

                        "step_4": "🟢 🟢 🟢 🔘 ⚪ ⚪\n\n"
                        "🔸 Passo 4. Indique quem você procura ⚧️",

                        "step_5": "🟢 🟢 🟢 🟢 🔘 ⚪\n\n"
                        "🔸 Passo 5. Envie sua foto 🤳"
                        "\n<i>De preferência um selfie em que seu rosto apareça bem</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Passo 6. Fale um pouco sobre você 📝"
                        "\n<i>Seja breve — 2 ou 3 frases</i>",
                        
                        "username_error": "⚠️ Para usar o bot, você precisa definir um <b>username</b> no Telegram."
                        "\nComo fazer:"
                        "\n1️⃣ Abra o Telegram → Configurações → Nome de usuário (tg://settings/username)"
                        "\n2️⃣ Crie um <b>Nome de usuário</b> único"
                        "\n3️⃣ Salve ✅"
                        "\nDepois volte no bot e clique em \"Repetir cadastro\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passo 6 não concluído"
                        "\nMínimo — {MIN_COUNT_SYMBOLS} caracteres"
                        "\nVocê escreveu {text_length} caracteres"
                        "\nTente escrever um pouco mais e envie de novo",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passo 6 não concluído."
                        "\nLimite: máximo {MAX_COUNT_SYMBOLS} caracteres."
                        "\nVocê escreveu {text_length}."
                        "\nTente resumir e envie de novo",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nSobre mim: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Se você usa o Telegram no PC, faça este passo no celular</i>",
                        "waiting": "Aguardando ...",
                        },
       
        "notifications":{"18year":"Boa! Você confirmou que tem mais de 18 anos",
                         "gender": "Legal! Você escolheu: {user_gender}",
                         "gender_search": "Legal! Você procura: {gender_search}",
                         "not_found": "Ainda não achamos ninguém na sua região 😔",
                         "not_username": "Faltando nome de usuário ❌",
                         "reloaded": "Menu atualizado 🔄",
                         "empty": "Nada encontrado",
                         "LOVE": "Você quer sair com {name}",
                         "SEX": "Você quer {name}",
                         "CHAT": "Você quer conversar com {name}",
                         "SKIP": "Você pulou {name}",
                         "delete": "Usuário excluído ❌",
                         "payment_sent": "Pagamento enviado ⭐️",
                         "unavailable": "A conta de {name} não está disponível 🚫",
                         "incognito" : {
                             True: "Modo Anônimo ativado ✅",
                             False: "Modo Anônimo desativado 🚫"},
                         },
        "match_menu":{"start": "Aqui você pode ver:"
                      "\n🔹 Combinações - quando os interesses batem"
                      "\n🔹 Coleção - perfis que você desbloqueou"
                      "\n🔹 Reações de outras pessoas ao seu perfil",
                      "you_want": "Vocês dois querem {reaction}",
                      "empty": {"LOVE": "Aqui vão aparecer pessoas que querem um ☕ <b>Encontro</b> com você",
                                "SEX": "Aqui vão aparecer pessoas que querem ir pra 👩‍❤️‍💋‍👨 <b>Cama</b> com você",
                                "CHAT": "Aqui vão aparecer pessoas que querem 💬 <b>Conversar</b> com você"},
                      "match_empty": "Aqui vão aparecer pessoas com quem seus interesses bateram"
                                    "\nAí você pode mandar uma msg ✉️",
                      "collection_empty": "Sua coleção está vazia"
                                           "\nAdicione perfis à coleção ✨."
                                           "\nVocê pode mandar msg ✉️"},
        "search_menu":{"start": "🔍 Buscar parceiro(a)",
                       "not_found": "Ainda não achamos ninguém na sua região 😔"
                       "\nTente mais tarde ☕"},
        "payment": {"incognito":{"label": "Ativar Modo Anônimo",
                                 "title": "Ativar Modo Anônimo",
                                "description": "Pague uma vez só — ative/desative quando quiser!"
                                "\nNesse modo você não aparece na busca, mas pode ver os outros perfis."},

                    "collection": {"label": "Adicionar {target_name} à ✨ Coleção",
                                   "title": "Adicionar {target_name} à ✨ Coleção",
                                   "description": "Ao adicionar à ✨ Coleção, você desbloqueia o perfil de {target_name} e pode mandar msg"}
        }}


BUTTONS_TEXT = {"begin":"Começar ✅",
                "reload": "Atualizar 🔄",
                "back":"⬅️ Voltar",
                "next":"Avançar ➡️",
                "return":"⏮️ Voltar ao menu",
                "delete": "🗑️ Excluir perfil",
                "search_menu": {"start":"🔍 Buscar"},
                "pay": "Pagar com Stars ⭐️",
                "reaction": {"LOVE":"☕ Encontro",
                             "SEX":"🔥 Cama",
                             "CHAT": "💬 Bater papo",
                             "SKIP":"Pular ⏩"},
                "match_menu":{"start":"💘 Ver combinações",
                              "match":"💘 Combinações [{match_count}]",
                              "collection":"✨ Coleção [{collection_count}]",
                              "love":"Encontros [{love_count}]",
                              "sex":"Cama [{sex_count}]",
                              "chat":"Conversas [{chat_count}]",
                              "add_to_collection":"Adicionar à Coleção {amount} ⭐️",
                              "send_message":"✉️ Enviar msg"},
                "gender": {"man": "Homem 🧔🏻",
                           "woman":"Mulher 👩🏻‍🦰",
                           "any":"Outro 👱"},
                "gender_search": {"man": "Procuro homem 🧔🏻",
                                  "woman":"Procuro mulher 👩🏻‍🦰",
                                  "any":"Tanto faz 🧔🏻👩🏻‍🦰👱"},
                "incognito":{"not_active":"🫥 Ficar Anônimo",
                             "on":"✅ Anônimo ligado",
                             "off":"🚫 Anônimo desligado",
                             },
                "profile":{"edit":"✏ Editar perfil",
                           "retry":"🔄 Repetir cadastro"},
                "location":{"send":"📍 Enviar localização",
                            "press":"📍 Toque para enviar"}
                }


# 👩‍❤️‍💋‍👨 🧔 👩 👤


GENDER_LABELS = {
    Gender.MAN: "Homem 🧔🏻",
    Gender.WOMAN: "Mulher 👩🏻‍🦰",
    Gender.ANY: "Outro 👱",
}


GENDER_SEARCH_LABELS = {
    Gender.MAN: "Procuro homem 🧔🏻",
    Gender.WOMAN: "Procuro mulher 👩🏻‍🦰",
    Gender.ANY: "Tanto faz 🧔🏻👩🏻‍🦰👱",
}


GENDER_EMOJI = {
    Gender.MAN: "♂️",
    Gender.WOMAN: "♀️",
    Gender.ANY: "⚧️",
}
