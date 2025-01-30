import faiss
import numpy as np
import pickle
import os
from pathlib import Path
from config import BASE_DIR, EMBEDDING_DIMENSION

class VectorDB:
    def __init__(self, dimension=EMBEDDING_DIMENSION):
        """
        Inicializa o banco de dados vetorial FAISS.
        
        Args:
            dimension (int): Dimensão dos embeddings. Padrão é 384 (dimensão do all-MiniLM-L6-v2).
        """
        self.index = faiss.IndexFlatL2(dimension)  # Índice FAISS para busca por similaridade
        self.metadata = []  # Armazena metadados associados aos embeddings
        self.dimension = dimension  # Dimensão dos embeddings

    def add_embeddings(self, embeddings, metadata):
        """
        Adiciona embeddings e metadados ao banco de dados.
        
        Args:
            embeddings (list): Lista de embeddings (cada embedding é uma lista de floats).
            metadata (list): Lista de metadados associados aos embeddings.
        
        Raises:
            ValueError: Se a dimensão dos embeddings for inconsistente.
        """
        if embeddings:
            # Verifica a dimensão de cada embedding
            for i, embedding in enumerate(embeddings):
                if len(embedding) != self.dimension:
                    raise ValueError(f"Embedding {i} tem dimensão {len(embedding)}, mas esperava-se {self.dimension}")
            
            # Converte os embeddings para um array numpy e adiciona ao índice FAISS
            vectors = np.array(embeddings).astype('float32')
            self.index.add(vectors)
            
            # Adiciona metadados
            self.metadata.extend(metadata)

    def save(self, filename='codebase_index'):
        """
        Salva o índice FAISS e os metadados em arquivos.
        
        Args:
            filename (str): Nome base dos arquivos de índice e metadados.
        """
        # Salva o índice FAISS
        faiss.write_index(self.index, str(BASE_DIR / f'{filename}.faiss'))
        
        # Salva os metadados
        with open(BASE_DIR / f'{filename}_meta.pkl', 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self, filename='codebase_index'):
        """
        Carrega o índice FAISS e os metadados de arquivos.
        
        Args:
            filename (str): Nome base dos arquivos de índice e metadados.
        
        Raises:
            FileNotFoundError: Se os arquivos de índice ou metadados não existirem.
        """
        # Caminhos dos arquivos
        faiss_file = BASE_DIR / f'{filename}.faiss'
        meta_file = BASE_DIR / f'{filename}_meta.pkl'
        
        # Verifica se os arquivos existem
        if not faiss_file.exists() or not meta_file.exists():
            raise FileNotFoundError(f"Arquivos de índice não encontrados: {faiss_file}, {meta_file}")
        
        # Carrega o índice FAISS
        self.index = faiss.read_index(str(faiss_file))
        
        # Carrega os metadados
        with open(meta_file, 'rb') as f:
            self.metadata = pickle.load(f)

    def search(self, query_embedding, k=5):
        """
        Realiza uma busca por similaridade no banco de dados.
        
        Args:
            query_embedding (list): Embedding da consulta.
            k (int): Número de resultados a retornar.
        
        Returns:
            list: Lista de tuplas (metadados, distância) dos resultados mais próximos.
        
        Raises:
            ValueError: Se a dimensão do embedding da consulta for inconsistente.
        """
        # Verifica a dimensão do embedding da consulta
        if len(query_embedding) != self.dimension:
            raise ValueError(f"Dimensão do embedding da consulta ({len(query_embedding)}) não corresponde à dimensão do índice ({self.dimension})")
        
        # Realiza a busca no índice FAISS
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)

        # Filtrar índices inválidos
        valid_results = []
        for i, index in enumerate(indices[0]):
            if 0 <= index < len(self.metadata):  # Verifica se o índice está dentro do range válido
                valid_results.append((self.metadata[index], distances[0][i]))

        if not valid_results:
            raise ValueError("Nenhum resultado válido foi encontrado na base de dados.")

        return valid_results
