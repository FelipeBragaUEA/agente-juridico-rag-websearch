🚀 Sistema de Repositório Jurídico com FastMCP

Este guia explica o processo de configuração e execução do sistema, que é dividido em três fases principais: Ingestão de Dados, Inicialização do Servidor de Backend (FastMCP) e Execução da Aplicação Principal (app.py).

O sistema utiliza um servidor FastMCP (serviço de backend especializado) para consultas e uma aplicação Python (app.py) contendo a lógica do Agente e a função proxy que interliga os serviços.

🛠️ 1. Configuração Inicial e Dependências

1.1. Pré-requisitos

Certifique-se de que você tem os seguintes softwares instalados no seu ambiente local:

Python 3.x

pip (Gerenciador de pacotes do Python)

1.2. Instalação das Dependências

O arquivo requirements.txt lista todas as bibliotecas Python necessárias (como FastAPI, Uvicorn, bibliotecas para embeddings, etc.).

Execute o comando abaixo no terminal, dentro do diretório raiz do projeto, para instalar todas as dependências:

pip install -r requirements.txt


📂 2. Etapa de Ingestão de Dados (Ingestão Jurídica)

Esta etapa é obrigatória e deve ser executada apenas uma vez (ou sempre que houver atualização nas fontes de dados jurídicos). Ela prepara os documentos para a consulta.

2.1. Execução do Script de Ingestão

Execute o script responsável pelo carregamento e processamento dos documentos:

python ingestaojuri.py


Processo: Este script lê suas fontes de dados, aplica processamento de linguagem natural (tokenização, indexação, embedding vetorial) e armazena os dados em um formato consultável pelo FastMCP.

Aguarde: O processo pode levar alguns minutos, dependendo do volume de dados. Espere a mensagem de conclusão antes de prosseguir.

📡 3. Iniciando os Serviços

O sistema requer que dois componentes rodem em paralelo: o servidor de backend e a aplicação principal.

3.1. Servidor FastMCP (Backend)

Inicie o servidor de backend que hospeda a lógica de consulta especializada.

Execute o comando em um terminal:

uvicorn mcserver:app --host 127.0.0.1 --port 8000


O servidor iniciará, escutando requisições no endereço http://127.0.0.1:8000.

Ajuste: Se o seu arquivo principal ou variável de aplicação FastAPI for diferente, altere mcserver:app.

⚠️ Atenção: Mantenha este terminal aberto e rodando. Você deve abrir um novo terminal para a próxima etapa.

3.2. Programa Principal (Aplicação Final)

Com o servidor FastMCP ativo, inicie o Agente da aplicação principal.

Execute o comando no novo terminal:

python app.py


Comunicação: O app.py iniciará a interface/lógica do Agente. Quando uma consulta jurídica é feita, a função proxy em app.py envia automaticamente uma requisição HTTP POST para o FastMCP em http://127.0.0.1:8000/mcp/... e aguarda a resposta para apresentá-la ao usuário.
