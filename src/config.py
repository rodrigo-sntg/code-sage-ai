import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CODEBASE_ROOT = "/home/rodrigos/ntconsult/projects/ms-claims"  # Altere para seu caminho
IGNORE_DIRS = {'.git', 'build', 'target', '.idea', 'node_modules'}
FILE_EXTENSIONS = {'.java', '.md', '.txt', '.xml'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
CHUNK_SIZE = 4000  # Tokens
OVERLAP = 200  # Tokens
OLLAMA_ENDPOINT = "http://localhost:11434/api"
EMBEDDING_MODEL = "nomic-embed-text:latest"
EMBEDDING_DIMENSION = 768