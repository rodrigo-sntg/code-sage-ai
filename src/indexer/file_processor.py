import os
from tqdm import tqdm
from config import CODEBASE_ROOT, IGNORE_DIRS, FILE_EXTENSIONS, MAX_FILE_SIZE, CHUNK_SIZE,OVERLAP

class FileProcessor:
    @staticmethod
    def get_files():
        files = []
        for root, dirs, filenames in os.walk(CODEBASE_ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if FileProcessor._is_valid_file(filepath):
                    files.append(filepath)
        return files

    @staticmethod
    def _is_valid_file(filepath):
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            return False
        ext = os.path.splitext(filepath)[1].lower()
        return ext in FILE_EXTENSIONS

    @staticmethod
    def chunk_file(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        chunks = []
        start = 0
        while start < len(content):
            end = start + CHUNK_SIZE
            chunk = content[start:end]
            chunks.append({
                'text': chunk,
                'metadata': {
                    'filepath': filepath,
                    'start_line': start // 80,  # Aproximação
                    'end_line': end // 80
                }
            })
            start = end - OVERLAP
        return chunks