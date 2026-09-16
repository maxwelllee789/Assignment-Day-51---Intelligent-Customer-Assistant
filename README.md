# Intelligent Customer Assistant

RAG (Retrieval-Augmented Generation) chatbot buat customer support — jawab pertanyaan pelanggan berdasarkan knowledge base yang disimpan di PostgreSQL + pgvector, dengan LLM dari Groq.

## Struktur Project

```
.
├── app.py              # UI chat (Streamlit)
├── rag.py               # Core RAG: retrieval + generation
├── database.py          # Koneksi & setup vector store (pgvector)
├── embeddings.py        # Konfigurasi embedding model
├── ingest.py            # Load dataset -> masukin ke vector store
├── init_database.py     # Bikin tabel vector store di Postgres
├── test_retrieval.py     # Test retrieval langsung ke vector store
├── requirements.txt
└── dataset_assignment - Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv
```

## Cara Kerja

### 1. Dataset

Pakai **Bitext Sample Customer Support Training Dataset** (kolom `prompt` & `response`, konten customer support asli). `ingest.py` baca CSV ini, ambil `ROW_LIMIT` baris pertama (default 150, bisa dinaikkan), dan susun tiap baris jadi satu `Document` dengan format:

```
Q: <prompt>
A: <response>
```

beserta metadata (`knowledge_id`, `category`, `title`, `source`).

### 2. Storing — PostgreSQL + pgvector

- `database.py` konek ke Postgres via `DATABASE_URL` (dari `.env`), pakai `langchain_postgres` (`PGEngine` + `PGVectorStore`), tabel bernama **`assignment51_knowledge`**.
- `init_database.py` bikin tabel vector store-nya (dengan ukuran vector sesuai dimensi embedding model yang dipakai).
- `embeddings.py` pakai **FastEmbedEmbeddings** dengan model `BAAI/bge-small-en-v1.5`.
- `ingest.py` embed semua dokumen dari dataset lalu `vector_store.add_documents()` — simpan ke tabel di atas.

### 3. RAG (Retrieval + Generation)

`rag.py`:
1. `vector_store.similarity_search(question, k=3)` — ambil 3 dokumen paling relevan dari Postgres.
2. Susun jadi context (title, isi, source per dokumen).
3. Kirim ke LLM **Groq** (`openai/gpt-oss-20b`, temperature 0) lewat prompt yang mewajibkan jawaban:
   - dalam Bahasa Indonesia,
   - hanya berdasarkan context (nggak boleh ngarang),
   - kalau info nggak ada di context, bilang terus terang belum tersedia,
   - nggak boleh ngaku sebagai karyawan resmi perusahaan manapun.
4. Return jawaban + daftar sumber (dokumen yang dipakai).

### 4. UI

`app.py` — chat interface pakai **Streamlit**. Nyimpen histori chat di `st.session_state`, dan tiap jawaban ada expander **"📚 Sumber informasi"** yang nunjukin dokumen sumber yang dipakai buat jawab.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Buat file `.env`:
   ```
   DATABASE_URL=<connection string PostgreSQL, contoh: postgresql+psycopg://user:pass@localhost:5433/assignment51>
   GROQ_API_KEY=<Groq API key>
   ```
3. Pastikan Postgres + ekstensi pgvector udah jalan (misal via Docker).
4. Bikin tabel vector store:
   ```bash
   python init_database.py
   ```
5. Ingest dataset ke vector store:
   ```bash
   python ingest.py
   ```

## Menjalankan

- **Cek retrieval aja** (tanpa generation):
  ```bash
  python test_retrieval.py
  ```
- **Chat lewat terminal**:
  ```bash
  python rag.py
  ```
- **Chat lewat UI Streamlit**:
  ```bash
  streamlit run app.py
  ```

## Tools yang Digunakan

- Langchain (`langchain_core`, `langchain_postgres`, `langchain_groq`, `langchain_community`)
- PostgreSQL + pgvector — vector database
- FastEmbedEmbeddings (`BAAI/bge-small-en-v1.5`) — embedding model
- Groq (`openai/gpt-oss-20b`) — LLM generation
- Streamlit — UI chat
