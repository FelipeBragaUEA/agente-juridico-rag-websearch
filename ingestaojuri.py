import os
import warnings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- IMPORT ---
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- CONFIGURAÇÃO ---
DATA_PATH = "documentos_juridicos/"  
CHROMA_PATH = "chroma_db_juridico"  

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()

def carregar_e_indexar_documentos():
    """Carrega PDFs, divide, gera embeddings LOCALMENTE e salva no ChromaDB."""
    print(f"🚀 Iniciando a ingestão de documentos na pasta: {DATA_PATH}")

    if not os.path.exists(DATA_PATH):
        print(f"❌ ERRO: Crie a pasta '{DATA_PATH}' e adicione seus PDFs jurídicos (Contratos, Códigos, Leis).")
        return

    # 1. Carregar os documentos PDF
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        print("⚠️ Atenção: NENHUM PDF encontrado na pasta. O RAG não funcionará.")
        return

    print(f"✅ Documentos carregados: {len(documents)} páginas encontradas.")

    # 2. Dividir o texto em chunks (pedaços)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=250,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Texto dividido em {len(chunks)} chunks para indexação.")

    # 3. Criar Embeddings (Modelo Local) e Indexar no ChromaDB
    print("⏳ Gerando Embeddings e construindo o Vector Store...")
    
    # Usando Embeddings Locais (sentence-transformers)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Cria o banco vetorial e o salva no disco
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    db.persist() 
    print(f"🎉 INGESTÃO CONCLUÍDA! Vector Store salvo em '{CHROMA_PATH}' com {len(chunks)} itens.")

if __name__ == "__main__":
    carregar_e_indexar_documentos()