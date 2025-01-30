import requests
import json
from tqdm import tqdm
from config import OLLAMA_ENDPOINT, EMBEDDING_MODEL

class EmbeddingGenerator:
    @staticmethod
    def get_embeddings(texts):
        embeddings = []
        for text in tqdm(texts, desc="Gerando embeddings"):
            try:
                # Faz a requisição para a API do Ollama
                response = requests.post(
                    f"{OLLAMA_ENDPOINT}/embeddings",
                    json={
                        'model': EMBEDDING_MODEL,
                        'prompt': text
                    },
                    timeout=30  # Timeout de 30 segundos
                )

                # Verifica se a requisição foi bem-sucedida
                if response.status_code == 200:
                    response_data = response.json()
                    if 'embedding' in response_data:
                        embeddings.append(response_data['embedding'])
                    else:
                        raise ValueError(f"Resposta da API não contém 'embedding': {response_data}")
                else:
                    raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão ao gerar embedding: {e}")
                continue  # Continua para o próximo texto

        # Verifica se todos os embeddings têm a mesma dimensão
        if embeddings:
            embedding_dim = len(embeddings[0])
            for i, embedding in enumerate(embeddings):
                if len(embedding) != embedding_dim:
                    raise ValueError(f"Embedding {i} tem dimensão {len(embedding)}, mas esperava-se {embedding_dim}")

        return embeddings