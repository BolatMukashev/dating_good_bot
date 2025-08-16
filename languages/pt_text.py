from models import Gender


TEXT = {"user_profile":{"step_1": "🔘 ⚪ ⚪ ⚪ ⚪ ⚪\n\n"
                        "Olá, <b>{first_name}</b>!\n"
                        "Pronto(a) para novas conexões?\n\n"
                        "Para começar, siga alguns passos simples:\n\n"
                        "🔸 Passo 1. Ao clicar em «Iniciar cadastro», você:"
                        "\n🔹Confirma que tem mais de 18 anos 🪪"
                        '\n🔹Aceita o <a href="{notion_site}">Termo de Uso</a>'
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
                        "\n<i>De preferência um selfie onde seu rosto apareça bem</i>",

                        "step_6": "🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "🔸 Passo 6. Fale um pouco sobre você 📝"
                        "\n<i>Tente ser breve — 2 a 3 linhas</i>",
                        
                        "username_error": "⚠️ Para usar o bot, é necessário definir um <b>username</b> no Telegram."
                        "\nComo fazer isso:"
                        "\n1️⃣ Abra Telegram → Configurações → Nome de usuário (tg://settings/username)"
                        "\n2️⃣ Crie um <b>Nome de usuário</b> único"
                        "\n3️⃣ Salve as alterações ✅"
                        "\nDepois volte ao bot e clique em \"Repetir cadastro\"",

                        "min_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passo 6 não concluído"
                        "\nMínimo — {MIN_COUNT_SYMBOLS} caracteres"
                        "\nVocê escreveu {text_length} caracteres"
                        "\nTente complementar a descrição e envie novamente",

                        "max_count_symbols_error":"🟢 🟢 🟢 🟢 🟢 🔘\n\n"
                        "❌ Passo 6 não concluído."
                        "\nLimite excedido: máximo — {MAX_COUNT_SYMBOLS} caracteres."
                        "\nVocê escreveu {text_length} caracteres."
                        "\nTente resumir a descrição e envie novamente",
                        
                        "profile": "🪪 <b>{first_name}</b>"
                        "\n📌 {country_local}, {city_local}"
                        "\n{gender_emoji} {gender}"
                        "\n🔍 {gender_search}"
                        "\nSobre mim: <i>{about_me}</i>",
                        
                        "get_location_message": "<i>Se você usa o Telegram no computador, faça este passo no celular</i>",
                        "waiting": "Aguardando ...",
                        },
       
        "notifications":{"18year":"Perfeito! Você confirmou que tem mais de 18 anos",
                         "gender": "Ótimo! Você escolheu: {user_gender}",
                         "gender_search": "Ótimo! Você procura: {gender_search}",
                         "not_found": "Ainda não encontramos ninguém na sua região 😔",
                         "not_username": "Nome de usuário ausente ❌",
                         "reloaded": "Menu atualizado 🔄",
                         "empty": "Nada encontrado",
                         "LOVE": "Você quer um encontro com {name}",
                         "SEX": "Você quer {name}",
                         "CHAT": "Você quer conversar com {name}",
                         "SKIP": "Você pulou {name}",
                         "delete": "Usuário removido ❌",
                         "payment_sent": "Pagamento enviado ⭐️",
                         "unavailable": "A conta de {name} não está disponível agora 🚫",
                         "incognito" : {
                             True: "Modo Anônimo ativado ✅",
                             False: "Modo Anônimo desativado 🚫"},
                         },
        "match_menu":{"start": "Aqui você pode ver:"
                      "\n🔹 Combinações - quando seus interesses coincidem"
                      "\n🔹 Coleção - perfis aos quais você tem acesso"
                      "\n🔹 Reações de outras pessoas ao seu perfil",
                      "you_want": "Vocês dois querem {reaction}",
                      "empty": {"LOVE": "Aqui aparecerão pessoas que querem um ☕ <b>Encontro</b> com você",
                                "SEX": "Aqui aparecerão pessoas que querem ir para a 👩‍❤️‍💋‍👨 <b>Cama</b> com você",
                                "CHAT": "Aqui aparecerão pessoas que querem 💬 <b>Conversar</b> com você"},
                      "match_empty": "Aqui aparecerão pessoas com quem seus desejos coincidiram"
                                    "\nVocê poderá enviar uma mensagem ✉️",
                      "collection_empty": "Sua coleção está vazia"
                                           "\nAdicione perfis à coleção ✨."
                                           "\nVocê poderá enviar mensagens ✉️"},
        "search_menu":{"start": "🔍 Encontrar parceiro(a)",
                       "not_found": "Ainda não encontramos ninguém na sua região 😔"
                       "\nTente novamente mais tarde ☕"},
        "payment": {"incognito":{"label": "Ativar Modo Anônimo",
                                 "title": "Ativar Modo Anônimo",
                                "description": "Compre uma vez — ative/desative quando quiser!"
                                "\nNesse modo você não aparece na busca, mas pode ver os perfis dos outros."},

                    "collection": {"label": "Adicionar {target_name} à ✨ Coleção",
                                   "title": "Adicionar {target_name} à ✨ Coleção",
                                   "description": "Ao adicionar à ✨ Coleção, você terá acesso ao perfil de {target_name} e poderá enviar mensagem"}
        }}


BUTTONS_TEXT = {"begin":"Iniciar ✅",
                "reload": "Atualizar 🔄",
                "back":"⬅️ Voltar",
                "next":"Avançar ➡️",
                "return":"⏮️ Voltar ao menu",
                "delete": "🗑️ Excluir perfil",
                "search_menu": {"start":"🔍 Buscar"},
                "pay": "Pagar com Telegram Stars ⭐️",
                "reaction": {"LOVE":"☕ Encontro",
                             "SEX":"🔥 Cama",
                             "CHAT": "💬 Conversar",
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
                            "press":"📍 Clique para enviar"}
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
