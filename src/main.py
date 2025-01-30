from indexer.file_processor import FileProcessor
from indexer.embedding_generator import EmbeddingGenerator
from indexer.faiss_db import VectorDB
from query_handler.ollama_integration import OllamaHandler
from config import BASE_DIR, EMBEDDING_DIMENSION
import os
import time

def index_codebase():
    # Coletar arquivos
    files = FileProcessor.get_files()
    
    # Processar chunks
    chunks = []
    for file in files:
        chunks.extend(FileProcessor.chunk_file(file))
    
    # Gerar embeddings
    texts = [chunk['text'] for chunk in chunks]
    embeddings = EmbeddingGenerator.get_embeddings(texts)
    
    # Construir banco vetorial
    db = VectorDB(dimension=EMBEDDING_DIMENSION)
    db.add_embeddings(embeddings, chunks)
    db.save()
    
    return db

def query_codebase(db, question):
    # Embedding da pergunta
    query_embedding = OllamaHandler.get_query_embedding(question)
    
    # Verificar dimensão do embedding
    if len(query_embedding) != db.dimension:
        raise ValueError(f"Dimensão do embedding da consulta ({len(query_embedding)}) não corresponde à dimensão do índice ({db.dimension})")
    
    # Buscar contexto relevante
    results = db.search(query_embedding, k=5)
    
    # Construir contexto
    context = "\n\n".join([res[0]['text'] for res in results])
    
    # Gerar resposta
    return OllamaHandler.generate_response(question, context)

def check_index_exists():
    faiss_file = BASE_DIR / 'codebase_index.faiss'
    meta_file = BASE_DIR / 'codebase_index_meta.pkl'
    return faiss_file.exists() and meta_file.exists()

if __name__ == "__main__":
    # Verificar se o índice já existe
    if not check_index_exists():
        print("Índice não encontrado. Iniciando indexação do código...")
        db = index_codebase()
        print("Indexação concluída!")
    else:
        # Carregar banco existente
        print("Carregando índice existente...")
        db = VectorDB(dimension=EMBEDDING_DIMENSION)  # Garantir dimensão correta
        db.load()
    
    # Exemplo de consulta
    while True:
        question = input("\nPergunta: ")
        if question.lower() in ['sair', 'exit', 'quit']:
            break
        start_time = time.time()
        response = query_codebase(db, question)
        print(f"\nResposta ({time.time()-start_time:.2f}s):")
        print(response)