import streamlit as st
import os
import warnings
from datetime import date
from dotenv import load_dotenv 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate, BasePromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults



load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_PATH = "chroma_db_juridico"

warnings.filterwarnings("ignore", category=UserWarning)

# INICIALIZAÇÃO

@st.cache_resource
def inicializar_agente():

    if not GEMINI_API_KEY:
        st.error("❌ GEMINI_API_KEY não encontrada.")
        return None

    # LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0
    )

    # RAG LOCAL

    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
    except Exception as e:
        st.error(f"❌ Erro ao carregar Chroma: {e}")
        return None

    @tool
    def consultar_repositorio_juridico(consulta: str) -> str:
        """Consulta leis e códigos no repositório jurídico local."""
        docs = db.similarity_search(consulta, k=7)

        if not docs:
            return "Nenhum documento encontrado."

        saida = []
        for doc in docs:
            fonte = doc.metadata.get("source", "Desconhecida")
            saida.append(f"--- Fonte: {fonte} ---\n{doc.page_content}\n")

        return "\n".join(saida)

    # TAVILY

    tools = [consultar_repositorio_juridico]

    if TAVILY_API_KEY:
        tavily_tool = TavilySearchResults(
            max_results=3,
            tavily_api_key=TAVILY_API_KEY
        )
        tools.append(tavily_tool)

    # PROMPT REACT

    tool_names = ", ".join([t.name for t in tools])

    tools_rendered = "\n".join(
        [f"- {t.name}: {t.description}" for t in tools]
    )

    REACT_PROMPT_TEMPLATE = """
Você é um AGENTE CONSULTOR JURÍDICO ESPECIALISTA EM DIREITO BRASILEIRO.

Você DEVE usar as ferramentas para buscar leis e jurisprudência antes de responder.

Ferramentas disponíveis:
{tool_names}

Descrição das ferramentas:
{tools}

Hoje é: {today}

Formato obrigatório:

Question: pergunta
Thought: raciocínio
Action: ferramenta
Action Input: argumento
Observation: resultado
... (pode repetir)
Final Answer: resposta jurídica completa e fundamentada.

Question: {input}
{agent_scratchpad}
"""

    prompt: BasePromptTemplate = PromptTemplate.from_template(
        REACT_PROMPT_TEMPLATE
    )

    prompt = prompt.partial(
        tool_names=tool_names,
        tools=tools_rendered,
        today=str(date.today())
    )

    agent = create_react_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return executor


# INTERFACE STREAMLIT

st.set_page_config(
    page_title="Agente Jurídico",
    layout="wide"
)

st.title("⚖️ Agente Consultor Jurídico")
st.markdown("---")

agent_executor = inicializar_agente()

if agent_executor:

    consulta = st.text_area(
        "Digite sua pergunta jurídica:",
        "Quais as hipóteses de responsabilidade civil sem culpa e qual a lei aplicável?"
    )

    if st.button("Executar Consulta Fundamentada"):

        if not consulta.strip():
            st.warning("Digite uma pergunta.")
        else:
            with st.spinner("Executando análise jurídica..."):

                pergunta_react = f"""
Para a pergunta: "{consulta}"

1. Consulte as leis no repositório jurídico.
2. Consulte jurisprudência se necessário.
3. Gere resposta final completa, técnica e objetiva.
"""

                try:
                    resposta = agent_executor.invoke(
                        {"input": pergunta_react}
                    )

                    st.subheader("✅ Resposta Final")
                    st.markdown(resposta["output"])

                except Exception as e:
                    st.error(f"❌ Erro durante a execução: {e}")
