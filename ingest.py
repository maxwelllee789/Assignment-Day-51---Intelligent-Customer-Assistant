import csv
from langchain_core.documents import Document
from database import get_vector_store

CSV_PATH = "dataset_assignment - Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
ROW_LIMIT = 150  # ambil sebagian dulu, bisa dinaikkan nanti

def load_knowledge_base():
    documents = []

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for index, row in enumerate(reader, start=1):
            if index > ROW_LIMIT:
                break

            prompt = (row.get("prompt") or "").strip()
            response = (row.get("response") or "").strip()

            if not prompt or not response:
                continue

            content = f"Q: {prompt}\nA: {response}"

            document = Document(
                page_content=content,
                metadata={
                    "knowledge_id": index,
                    "category": "general",
                    "title": prompt[:80],
                    "source": CSV_PATH
                }
            )
            documents.append(document)

    return documents

def ingest():
    documents = load_knowledge_base()
    vector_store = get_vector_store()

    vector_store.add_documents(
        documents=documents
    )

    print(
        f"{len(documents)} documents berhasil dimasukkan."
    )

if __name__ == "__main__":
    ingest()