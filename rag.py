from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from database import get_vector_store

vector_store = get_vector_store()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful customer service assistant.

Answer the customer's question using ONLY the information
available in the provided context.

Rules:
1. Answer in Indonesian.
2. Use clear and friendly language.
3. Do not invent information that is not in the context.
4. If the answer is not available in the context, clearly say
   that the information is not available.
5. If necessary, suggest contacting official customer support.
6. Do not claim that you are an official employee of any company.
"""
        ),
        (
            "human",
            """
Context:
{context}

Customer question:
{question}
"""
        )
    ]
)

def format_documents(documents):
    formatted_context = []

    for document in documents:
        text = f"""
Title:
{document.metadata.get('title')}

Information:
{document.page_content}

Source:
{document.metadata.get('source')}
"""
        formatted_context.append(text)

    return "\n\n".join(formatted_context)

def ask_customer_assistant(question):
    documents = vector_store.similarity_search(
        question,
        k=3
    )

    context = format_documents(documents)

    messages = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "sources": documents
    }

if __name__ == "__main__":
    question = input("Customer question: ")

    result = ask_customer_assistant(question)

    print("\nANSWER")
    print(result["answer"])

    print("\nSOURCES")
    for source in result["sources"]:
        print("-", source.metadata.get("title"))