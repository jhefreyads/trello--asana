Integração Trello x Asana
Objetivo
Desenvolver uma integração entre Trello e Asana para sincronização de tarefas, convertendo quadros e listas do Trello em projetos e seções do Asana.
1. Análise das APIs

Trello

    •	Autenticação: API Key e Token

    •	Principais Endpoints: 

        o	Quadros: GET /1/members/me/boards

        o	Listas: GET /1/boards/{id}/lists

        o	Cartões: GET /1/lists/{id}/cards, POST /1/cards
        
Asana
  
    •	Autenticação: OAuth 2.0 (Token de Acesso Pessoal - PAT)

    •	Principais Endpoints: 

      o	Projetos: POST /projects 
        -	Campos Necessários: name (nome do projeto), notes (descrição do projeto)

      o	Seções: POST /projects/{project_gid}/sections 
        -	Campos Necessários: name (nome da seção), project (ID do projeto ao qual pertence)

      o	Tarefas: POST /tasks 
        -	Campos Necessários: name (nome da tarefa), notes (descrição), projects (ID do projeto), due_at (data de vencimento)

3. Mapeamento dos Campos (De-Para)
Trello	Asana	Observação
id	gid	Identificador único do objeto
name	name	Nome do quadro, lista ou cartão
desc	notes	Descrição do cartão para notas da tarefa
due	due_at	Data de vencimento do cartão para a tarefa


4. Fluxo de Integração
1.	Autenticação: 
o	Obter credenciais e autenticar nas APIs do Trello e Asana.
2.	Sincronização de Projetos: 
o	Buscar quadros no Trello e criar projetos no Asana com os campos name, team e notes.
3.	Sincronização de Seções: 
o	Buscar listas no Trello e criar seções no Asana associadas ao respectivo projeto.
4.	Sincronização de Tarefas: 
o	Buscar cartões no Trello e criar tarefas no Asana, garantindo que cada uma esteja vinculada ao projeto e seção correspondentes.
5.	Manutenção Contínua: 
o	Implementação de Webhooks para monitoramento de alterações.


4. Código prático
Junto com os arquivos, está um código em python funcional com a integração em questão.

5. Considerações Finais
A integração garante que as informações entre Trello e Asana permaneçam sincronizadas, facilitando a transição e o uso conjunto das duas ferramentas.

