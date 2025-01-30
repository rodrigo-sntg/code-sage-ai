import requests
import json
from config import OLLAMA_ENDPOINT, EMBEDDING_MODEL

class OllamaHandler:
    @staticmethod
    def generate_response(prompt, context):
        full_prompt = f"""Contexto do código:
        {context}

        Pergunta: {prompt}
        Resposta:"""
        
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={
                'model': 'deepseek-coder:6.7b',
                'prompt': full_prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'num_ctx': 16000
                }
            }
        )
        return response.json()['response']

    @staticmethod
    def get_query_embedding(query):
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/embeddings",
            json={
                'model': EMBEDDING_MODEL,
                'prompt': query
            }
        )
        return response.json()['embedding']