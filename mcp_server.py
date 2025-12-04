
from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from tavily import TavilyClient


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
CHROMA_PATH = "chroma_db_juridico"


server = FastMCP("servidor_juridico_mcp")


emb = SentenceTransformer("all-MiniLM-L6-v2")

client = PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="juridico",
    metadata={"tipo": "juridico"},
)

def _consultar_repositorio_juridico(consulta: str):
    try:
        results = collection.query(
            query_texts=[consulta],
            n_results=5,
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        saida = []
        for doc, meta in zip(docs, metas):
            fonte = meta.get("source", "Desconhecido")
            saida.append(f"--- Fonte: {fonte} ---\n{doc}\n")

        return {"resultado": "\n".join(saida)}

    except Exception as e:
        return {"erro": f"Falha ao consultar RAG: {e}"}


tavily = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None


def _pesquisar_jurisprudencia(consulta: str):
    if not tavily:
        return {"erro": "TAVILY_API_KEY não configurada."}

    try:
        resp = tavily.search(
            query=f"jurisprudência {consulta}",
            max_results=5
        )

        saida = []
        for entry in resp["results"]:
            saida.append(
                f"Título: {entry['title']}\n"
                f"Resumo: {entry.get('snippet', '')}\n"
                f"Fonte: {entry['url']}\n\n"
            )

        return {"resultado": "\n".join(saida)}

    except Exception as e:
        return {"erro": f"Erro ao consultar Tavily: {e}"}



@server.tool()
def consultar_repositorio_juridico(consulta: str):
    return _consultar_repositorio_juridico(consulta)


@server.tool()
def pesquisar_jurisprudencia(consulta: str):
    return _pesquisar_jurisprudencia(consulta)


app = FastAPI(title="MCP Jurídico API")


@app.post("/tools/consultar_repositorio_juridico")
def api_rag(payload: dict):
    return _consultar_repositorio_juridico(payload["consulta"])


@app.post("/tools/pesquisar_jurisprudencia")
def api_web(payload: dict):
    return _pesquisar_jurisprudencia(payload["consulta"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
