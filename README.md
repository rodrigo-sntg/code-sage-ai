# AI-Trained Codebase Assistant

This project allows you to index a codebase (especially Java projects) and use a language model (like Deepseek or Ollama) to answer questions about the code, understand the business context, and assist in developing new features.

## Features

- **Code Indexing**: Splits code into chunks and generates embeddings for each part.
- **Semantic Search**: Enables searching for relevant code snippets based on embeddings.
- **Contextual Responses**: Uses a language model to answer questions based on the indexed code.
- **Java Project Support**: Focused on Java projects but can be adapted for other languages.

## Prerequisites

- Python 3.8 or higher.
- [Ollama](https://ollama.ai/) installed and configured.
- Language and embedding models downloaded (e.g., `deepseek-coder:33b` and `nomic-embed-text`).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-trained-codebase-assistant.git
   cd ai-trained-codebase-assistant
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Download the required models in Ollama:
   ```bash
   ollama pull deepseek-coder:33b
   ollama pull nomic-embed-text
   ```

## Configuration

1. Edit the `config.py` file to define your codebase path and other settings:
   ```python
   CODEBASE_ROOT = "/path/to/your/project"  # Change to your project's path
   IGNORE_DIRS = {'.git', 'build', 'target', '.idea', 'node_modules'}  # Directories to ignore
   FILE_EXTENSIONS = {'.java', '.md', '.txt', '.xml'}  # File extensions to process
   ```

2. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

## Usage

### 1. Index the Codebase

Run the script to index the code:
```bash
python main.py
```

On the first run, the script will:
- Collect project files.
- Split files into chunks.
- Generate embeddings for each chunk.
- Save the FAISS index and metadata.

### 2. Ask Questions

After indexing, you can ask questions about the code:
```bash
Question: How many tests are in the project?
Answer (0.45s): There are 15 unit tests and 5 integration tests in the project.
```

### 3. Update the Index

If you add new files to the project, delete the existing index files and run the script again:
```bash
rm codebase_index.faiss codebase_index_meta.pkl
python main.py
```

## Project Structure

```
ai-trained-codebase-assistant/
├── indexer/
│   ├── file_processor.py       # Collects and splits files into chunks
│   ├── embedding_generator.py  # Generates embeddings for chunks
│   └── faiss_db.py             # Stores embeddings and enables semantic search
├── query_handler/
│   └── ollama_integration.py   # Integration with Ollama for generating responses
├── config.py                   # Project configuration
├── main.py                     # Main script
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Dependencies

- **Python**:
  - `requests`: For making HTTP requests to the Ollama API.
  - `faiss-cpu`: For creating and managing the vector database.
  - `numpy`: For array manipulation.
  - `tqdm`: For progress bars.
  - `python-dotenv`: For managing environment variables (optional).

- **Ollama**:
  - `deepseek-coder:33b`: Language model for generating responses.
  - `nomic-embed-text`: Model for generating embeddings.

## Example Questions

- "Where is the authentication service implemented?"
- "How many controllers are in the project?"
- "How does the payment system work?"
- "Show examples of unit tests."

