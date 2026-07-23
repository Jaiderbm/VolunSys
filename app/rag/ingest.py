import os
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    from langchain.vectorstores import Chroma

# Base paths relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "rag", "knowledge_base")
DB_DIR = os.path.join(BASE_DIR, "rag", "vector_store")

def run_ingestion():
    print(f"Buscando documentos en: {KNOWLEDGE_DIR}")
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)
        print(f"Carpeta creada: {KNOWLEDGE_DIR}. Por favor coloca archivos allí.")
        return

    # 1. Load documents from knowledge_base directory
    # Support both .md and .txt files
    documents = []
    
    # Custom load to avoid issues with DirectoryLoader encoding
    for filename in os.listdir(KNOWLEDGE_DIR):
        if filename.endswith(".md") or filename.endswith(".txt"):
            filepath = os.path.join(KNOWLEDGE_DIR, filename)
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                documents.extend(loader.load())
                print(f"Cargado exitosamente: {filename}")
            except Exception as e:
                print(f"Error al cargar {filename}: {e}")

    if not documents:
        print("No se encontraron documentos validos (.md o .txt) para ingerir.")
        return

    # 2. Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = text_splitter.split_documents(documents)
    print(f"Total de fragmentos (chunks) creados: {len(chunks)}")

    # 3. Initialize HuggingFace embeddings
    print("Inicializando modelo de embeddings HuggingFace (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create and persist Chroma Vector DB
    print(f"Guardando base de datos vectorial en: {DB_DIR}")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Base de datos vectorial creada y persistida con exito!")

if __name__ == "__main__":
    run_ingestion()
