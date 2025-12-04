🚀 README: Sistema de Repositório Jurídico com FastMCP
Este guia rápido explica como configurar e executar o seu sistema completo, que utiliza um servidor FastMCP (serviço de backend especializado) e uma aplicação principal em Python (app.py) contendo a lógica do Agente e do Proxy.

💻 1. Pré-requisitos
Certifique-se de ter os seguintes softwares instalados em seu ambiente:

Python 3.x

pip (gerenciador de pacotes do Python)

🛠️ 2. Instalação das Dependências
O arquivo requirements.txt lista todas as bibliotecas Python necessárias para que o programa funcione.

Para instalar todas as dependências do projeto, execute o seguinte comando no seu terminal, dentro do diretório raiz do projeto:

Bash

pip install -r requirements.txt
📂 3. Etapa de Ingestão de Dados (Ingestão Jurídica)
Esta etapa é obrigatória e única (a menos que seus dados mudem). Ela carrega e prepara os documentos jurídicos para que o servidor FastMCP possa consultá-los.

Como Rodar:
Execute o script de ingestão, que normalmente se chama ingestaojuri.py (ou nome similar):

Bash

python ingestaojuri.py
O que ele faz: Este script lê suas fontes de dados jurídicos, processa-as (por exemplo, tokenização, indexação, embedding) e as salva em um formato que o FastMCP pode consultar (como um banco de dados local ou um índice vetorial).

Aguarde: Espere até que o script retorne uma mensagem de sucesso, indicando que a ingestão foi concluída.

📡 4. Iniciando o Servidor FastMCP (Backend)
O FastMCP (provavelmente construído com FastAPI ou similar) é o servidor de backend que hospeda a lógica de consulta especializada. Ele deve estar ativo antes de a aplicação principal ser iniciada.

Como Rodar:
Se o seu servidor for baseado em Uvicorn/FastAPI, o comando típico será:

Bash

uvicorn mcserver:app --host 127.0.0.1 --port 8000
Ajuste: Se o nome do seu arquivo ou variável de aplicação for diferente, altere mcserver:app conforme necessário.

O que ele faz: O servidor começará a escutar requisições no endereço http://127.0.0.1:8000.

🚨 NOTA CRÍTICA: Mantenha este terminal aberto e rodando. Você precisará abrir um novo terminal para a próxima etapa.

▶️ 5. Rodando o Programa Principal (Aplicação Final)
Com o servidor FastMCP ativo (no primeiro terminal), você pode iniciar a aplicação principal (app.py), que contém a lógica do Agente e a função proxy que fará a ponte para o backend.

Como Rodar:
No novo terminal que você abriu, execute:

Bash

python app.py
Fluxo de Comunicação:

O app.py inicia a interface ou o Agente.

Quando uma consulta jurídica é feita, a função proxy envia um HTTP POST para o servidor FastMCP em http://127.0.0.1:8000/mcp/....

Recebe a resposta do FastMCP e a apresenta ao usuário.
