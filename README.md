🚀 README: Sistema de Repositório Jurídico com FastMCP
Este guia rápido explica como configurar e executar o seu sistema, que utiliza um servidor FastMCP e uma aplicação principal em Python (app.py).

💻 1. Pré-requisitos
Certifique-se de ter o Python 3.x e o pip instalados em seu sistema.

🛠️ 2. Instalação das Dependências
O arquivo requirements.txt lista todas as bibliotecas Python necessárias para que o programa funcione corretamente.

Para instalar todas as dependências, execute o seguinte comando no seu terminal, dentro do diretório do projeto:

Bash

pip install -r requirements.txt
📂 3. Etapa de Ingestão de Dados (Ingestão Jurídica)
Esta etapa é crucial para carregar os dados no repositório jurídico antes de o servidor ser iniciado.

Como Rodar:
Execute o script de ingestão, que provavelmente está contido em um arquivo chamado ingestaojuri.py (ou nome similar):

Bash

python ingestaojuri.py
O que ele faz: Este script lê suas fontes de dados jurídicos, processa-as (por exemplo, tokenização, indexação, embedding) e as salva em um formato que o FastMCP pode consultar (como um banco de dados local ou um índice vetorial).

Aguarde: Espere até que o script retorne uma mensagem de sucesso, indicando que a ingestão foi concluída.

📡 4. Iniciando o Servidor FastMCP
O FastMCP (provavelmente construído com FastAPI ou similar) é o servidor de backend que hospeda a lógica de consulta ao repositório jurídico. Ele precisa estar rodando para que a aplicação principal possa consultá-lo.

Como Rodar:
Se o seu servidor for baseado em Uvicorn/FastAPI, o comando típico será:

Bash

uvicorn mcserver:app --host 127.0.0.1 --port 8000
(Ajuste mcserver:app se o nome do seu arquivo ou variável de aplicação for diferente).

O que ele faz: O servidor começará a escutar requisições no endereço http://127.0.0.1:8000. Ele fica rodando em segundo plano.

💡 Nota: Mantenha este terminal aberto e rodando. Você precisará abrir um novo terminal para a próxima etapa.

▶️ 5. Rodando o Programa Principal (Aplicação Final)
Com o servidor FastMCP ativo, você pode iniciar o programa principal (app.py), que contém o Agente e a função proxy descrita, para começar a interagir com o sistema.

Como Rodar:
No novo terminal (enquanto o servidor FastMCP está rodando no primeiro terminal), execute:

Bash

python app.py
O que ele faz:

Inicia a interface ou o Agente.

Quando uma consulta jurídica é feita, ele usa a função proxy para enviar um HTTP POST para o servidor FastMCP em http://127.0.0.1:8000/mcp/....

Recebe a resposta e a apresenta ao usuário.
