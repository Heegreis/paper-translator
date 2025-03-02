import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from lightrag import LightRAG, QueryParam

# from sentence_transformers import SentenceTransformer
from lightrag.llm.ollama import ollama_embed
from lightrag.utils import EmbeddingFunc

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')

WORKING_DIR = './dickens'

if os.path.exists(WORKING_DIR):
    import shutil

    shutil.rmtree(WORKING_DIR)

os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    # 1. Initialize the GenAI Client with your Gemini API Key
    client = genai.Client(api_key=gemini_api_key)

    # 2. Combine prompts: system prompt, history, and user prompt
    if history_messages is None:
        history_messages = []

    combined_prompt = ''
    if system_prompt:
        combined_prompt += f'{system_prompt}\n'

    for msg in history_messages:
        # Each msg is expected to be a dict: {"role": "...", "content": "..."}
        combined_prompt += f'{msg["role"]}: {msg["content"]}\n'

    # Finally, add the new user prompt
    combined_prompt += f'user: {prompt}'

    # 3. Call the Gemini model
    time.sleep(4)  # 添加 4 秒延遲，符合 15 RPM 限制
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )

    # 4. Return the response text
    return response.text


rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embed(
            texts, embed_model='nomic-embed-text', host='http://localhost:11434'
        ),
    ),
)

file_path = 'markdown/2211.09119v2/2211.09119v2_revised.md'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

rag.insert(text)

response = rag.query(
    query='What is the main theme of the paper?',
    param=QueryParam(mode='hybrid', top_k=5, only_need_context=True),
)

print(response)
