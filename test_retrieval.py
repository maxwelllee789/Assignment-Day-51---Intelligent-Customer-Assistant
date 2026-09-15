from database import get_vector_store

vector_store = get_vector_store()

question = (
    "How can I cancel my order?"
)

results = vector_store.similarity_search(
    question,
    k=3
)

print("\nQUESTION")
print(question)

print("\nRETRIEVED DOCUMENTS")

for index, document in enumerate(
    results,
    start=1
):
    print("\n----------------")
    print(f"Result {index}")
    print("Title:", document.metadata.get("title"))
    print("Category:", document.metadata.get("category"))
    print("Content:", document.page_content)