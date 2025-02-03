import requests
import json

# 🔹 Função para pegar os dados do usuário no terminal
def obter_dados_usuario():
    print("📝 Por favor, insira as informações necessárias:")
    
    TRELLO_CHAVE_API = input("Chave da API do Trello: ")
    TRELLO_TOKEN = input("Token de acesso do Trello: ")
    ASANA_TOKEN_ACESSO = input("Token de acesso do Asana: ")
        
    return TRELLO_CHAVE_API, TRELLO_TOKEN, ASANA_TOKEN_ACESSO

# 📌 Função para pegar os espaços de trabalho do Asana
def obter_espacos_trabalho_asana(token_acesso):
    url = "https://app.asana.com/api/1.0/workspaces"
    cabecalho = {"Authorization": f"Bearer {token_acesso}"}
    resposta = requests.get(url, headers=cabecalho)
    
    if resposta.status_code != 200:
        print(f"⚠️ Erro ao obter espaços de trabalho do Asana: {resposta.text}")
        return []
    
    return resposta.json().get('data', [])

# 📌 Função para pegar os quadros do Trello
def obter_quadros_trello(chave_api, token):
    url = "https://api.trello.com/1/members/me/boards"
    parametros = {"key": chave_api, "token": token}
    resposta = requests.get(url, params=parametros)
    
    if resposta.status_code != 200:
        print(f"⚠️ Erro ao obter quadros do Trello: {resposta.text}")
        return []
    
    return resposta.json()

# 📌 Função para pegar as listas do Trello (essas listas viram seções no Asana)
def obter_listas_trello(id_quadro, chave_api, token):
    url = f"https://api.trello.com/1/boards/{id_quadro}/lists"
    parametros = {"key": chave_api, "token": token}
    resposta = requests.get(url, params=parametros)
    
    if resposta.status_code != 200:
        print(f"⚠️ Erro ao obter listas do Trello: {resposta.text}")
        return []
    
    return resposta.json()

# 📌 Função para pegar os cartões dentro de uma lista no Trello (esses cartões viram tarefas no Asana)
def obter_cartoes_trello(id_lista, chave_api, token):
    url = f"https://api.trello.com/1/lists/{id_lista}/cards"
    parametros = {"key": chave_api, "token": token}
    resposta = requests.get(url, params=parametros)
    
    if resposta.status_code != 200:
        print(f"⚠️ Erro ao obter cartões do Trello: {resposta.text}")
        return []
    
    return resposta.json()

# 📌 Criando um novo projeto no Asana com o workflow
def criar_projeto_asana(nome, id_espaco_trabalho, token_acesso, seções=None):
    url = "https://app.asana.com/api/1.0/projects"
    cabecalho = {"Authorization": f"Bearer {token_acesso}"}
    
    dados = {"data": {"name": nome, "workspace": id_espaco_trabalho}}
    if seções:
        dados["data"]["sections"] = seções  # Adicionar as seções ao projeto
    
    resposta = requests.post(url, headers=cabecalho, json=dados)
    
    if resposta.status_code == 201:
        print(f"✅ Projeto '{nome}' criado no Asana!")
        return resposta.json()["data"]["gid"]
    else:
        print(f"⚠️ Erro ao criar o projeto: {resposta.text}")
        return None

# 📌 Função para criar uma seção (lista) no Asana
def criar_secao_asana(id_projeto, nome_secao, token_acesso):
    url = f"https://app.asana.com/api/1.0/sections"
    cabecalho = {"Authorization": f"Bearer {token_acesso}"}
    dados = {"data": {"name": nome_secao, "project": id_projeto}}
    resposta = requests.post(url, headers=cabecalho, json=dados)
    
    if resposta.status_code == 201:
        print(f"✅ Seção '{nome_secao}' criada no Asana!")
        return resposta.json()["data"]["gid"]
    else:
        print(f"⚠️ Erro ao criar seção: {resposta.text}")
        return None

# 📌 Função para criar um espaço de trabalho no Asana
def criar_espaco_trabalho_asana(nome_espaco, token_acesso):
    url = "https://app.asana.com/api/1.0/workspaces"
    cabecalho = {"Authorization": f"Bearer {token_acesso}"}
    dados = {"data": {"name": nome_espaco}}
    resposta = requests.post(url, headers=cabecalho, json=dados)
    
    if resposta.status_code == 201:
        print(f"✅ Espaço de trabalho '{nome_espaco}' criado no Asana!")
        return resposta.json()["data"]["gid"]
    else:
        print(f"⚠️ Erro ao criar espaço de trabalho: {resposta.text}")
        return None


# 📌 Função para criar uma tarefa no Asana
def criar_tarefa_asana(nome_tarefa, id_projeto, id_secao, id_workspace, token_acesso):
    
    url = f"https://app.asana.com/api/1.0/tasks"
    cabecalho = {"Authorization": f"Bearer {token_acesso}"}
    
    dados = {
        "data": {
            "name": nome_tarefa, 
            "workspace": id_workspace,  # Adicionando o workspace
            "project": [id_projeto],  # Associando ao projeto
            "sections": [id_secao]  # Associando a tarefa a uma seção específica
        }
    }
    
    resposta = requests.post(url, headers=cabecalho, json=dados)
    
    if resposta.status_code == 201:
        print(f"✅ Tarefa '{nome_tarefa}' criada no Asana!")
    else:
        print(f"⚠️ Erro ao criar tarefa: {resposta.text}")

# 📌 Função principal que faz toda a mágica acontecer 🚀
def sincronizar_trello_para_asana():
    print("🔄 Iniciando a sincronização do Trello para o Asana...")

    # Perguntar dados ao usuário
    TRELLO_CHAVE_API, TRELLO_TOKEN, ASANA_TOKEN_ACESSO = obter_dados_usuario()

    # Tentar obter os espaços de trabalho do Asana
    espacos_asana = obter_espacos_trabalho_asana(ASANA_TOKEN_ACESSO)
    
    if not espacos_asana:
        print("⚠️ Não há espaços de trabalho no Asana. Deseja criar um novo espaço de trabalho?")
        resposta = input("Digite 'sim' para criar um novo espaço ou qualquer outra tecla para sair: ").strip().lower()
        if resposta == "sim":
            nome_espaco = input("Qual o nome do novo espaço de trabalho? ")
            id_espaco_trabalho = criar_espaco_trabalho_asana(nome_espaco, ASANA_TOKEN_ACESSO)
            if not id_espaco_trabalho:
                print("❌ Erro ao criar o espaço de trabalho no Asana. Abortando sincronização...")
                return
        else:
            print("❌ Nenhum espaço de trabalho encontrado e nenhum novo espaço foi criado. Abortando sincronização...")
            return
    else:
        print("Escolha o espaço de trabalho para transferir:")
        for i, espaco in enumerate(espacos_asana, 1):
            print(f"{i} - {espaco['name']}")
        
        opcao_espaco = int(input("Selecione o número do espaço de trabalho desejado: "))
        id_espaco_trabalho = espacos_asana[opcao_espaco - 1]["gid"]
    
    # 1️⃣ Obter todos os quadros do Trello
    quadros = obter_quadros_trello(TRELLO_CHAVE_API, TRELLO_TOKEN)
    if not quadros:
        print("❌ Erro ao obter quadros do Trello. Reiniciando...")
        return sincronizar_trello_para_asana()

    print("Escolha o quadro a ser copiado:")
    print("1 - Todos os quadros")
    for i, quadro in enumerate(quadros, 2):
        print(f"{i} - {quadro['name']}")
    opcao_quadro = int(input("Selecione o número do quadro desejado: "))

    if opcao_quadro == 1:
        # Copiar todos os quadros
        for quadro in quadros:
            print(f"🔹 Processando quadro: {quadro['name']}")
            listas = obter_listas_trello(quadro["id"], TRELLO_CHAVE_API, TRELLO_TOKEN)
            id_projeto_asana = criar_projeto_asana(quadro["name"], id_espaco_trabalho, ASANA_TOKEN_ACESSO)
            if id_projeto_asana:
                for lista_trello in listas:
                    nome_lista = lista_trello["name"]
                    print(f"🔹 Processando lista: {nome_lista}")
                    
                    # Criar a seção no Asana
                    id_secao_asana = criar_secao_asana(id_projeto_asana, nome_lista, ASANA_TOKEN_ACESSO)
                    
                    # Verifique se a seção foi criada com sucesso
                    if id_secao_asana:
                        # Agora, obtenha os cartões dessa lista no Trello
                        cartoes = obter_cartoes_trello(lista_trello["id"], TRELLO_CHAVE_API, TRELLO_TOKEN)
                        
                        # Criar as tarefas logo após a criação da seção
                        for cartao in cartoes:
                            print(f"🔹 Criando tarefa: {cartao['name']}")
                            criar_tarefa_asana(cartao["name"], id_secao_asana, id_projeto_asana, id_espaco_trabalho, ASANA_TOKEN_ACESSO)
    else:
        # Copiar um quadro específico
        quadro_selecionado = quadros[opcao_quadro - 2]
        print(f"🔹 Processando quadro: {quadro_selecionado['name']}")
        listas = obter_listas_trello(quadro_selecionado["id"], TRELLO_CHAVE_API, TRELLO_TOKEN)
        id_projeto_asana = criar_projeto_asana(quadro_selecionado["name"], id_espaco_trabalho, ASANA_TOKEN_ACESSO)
        if id_projeto_asana:
            for lista_trello in listas:
                nome_lista = lista_trello["name"]
                print(f"🔹 Processando lista: {nome_lista}")
                
                # Criar a seção no Asana
                id_secao_asana = criar_secao_asana(id_projeto_asana, nome_lista, ASANA_TOKEN_ACESSO)
                
                # Verifique se a seção foi criada com sucesso
                if id_secao_asana:
                    # Agora, obtenha os cartões dessa lista no Trello
                    cartoes = obter_cartoes_trello(lista_trello["id"], TRELLO_CHAVE_API, TRELLO_TOKEN)
                    
                    # Criar as tarefas logo após a criação da seção
                    for cartao in cartoes:
                        print(f"🔹 Criando tarefa: {cartao['name']}")
                        criar_tarefa_asana(cartao["name"], id_secao_asana, id_projeto_asana, id_espaco_trabalho, ASANA_TOKEN_ACESSO)

    print("✅ Sincronização concluída com sucesso!")

# Executando a função principal
sincronizar_trello_para_asana()
