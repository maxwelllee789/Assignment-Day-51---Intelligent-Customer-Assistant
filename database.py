import asyncio
import os
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from dotenv import load_dotenv
from langchain_postgres import PGEngine, PGVectorStore
from embeddings import get_embeddings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TABLE_NAME = "assignment51_knowledge"

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL tidak ditemukan di .env"
    )

engine = PGEngine.from_connection_string(
    url=DATABASE_URL
)

def get_vector_store():
    embeddings = get_embeddings()

    vector_store = PGVectorStore.create_sync(
        engine=engine,
        table_name=TABLE_NAME,
        embedding_service=embeddings
    )

    return vector_store