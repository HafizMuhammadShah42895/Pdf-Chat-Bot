
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import pickle
import os
import ffmpeg






def get_rag_chain(chroma_path: str, bm25_path: str = "bm25_chunks.pkl", custom_prompt: str = None, memory_buffer=None):
    embedding = OllamaEmbeddings(model="llama3")
    vectorstore = Chroma(persist_directory=chroma_path, embedding_function=embedding)
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    if not os.path.exists(bm25_path):
        raise FileNotFoundError(f"BM25 file not found at: {bm25_path}")
    with open(bm25_path, "rb") as f:
        bm25_chunks = pickle.load(f)

    bm25_retriever = BM25Retriever.from_documents(bm25_chunks)
    bm25_retriever.k = 5

    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )

    formatted_memory = ""
    if memory_buffer:
        for entry in memory_buffer:
            formatted_memory += f"User: {entry.question}\nAI: {entry.answer}\n"

    base_prompt = """
Use the relevant document context and previous conversation history to answer the question clearly and concisely.

If the answer cannot be determined exactly from the provided context or conversation history, respond only with:
I don't know

Do not add explanations, guesses, or general background information when the answer is unknown.

Format the entire answer using plain text and simple HTML only:
- Use <strong> for bold text.
- Use <ul> and <li> for lists.
- Use <br> for line breaks.
- Do not use Markdown formatting.
- Keep the language simple, clear, and directly relevant to the question.
- Avoid repeating the question unless it is necessary for clarity.
Conversation History:
{memory}

Relevant Context:
{context}

Question:
{question}
    """.strip()

    if custom_prompt:
        base_prompt += f"\n\n# Additional Instructions:\n{custom_prompt}"

    prompt = PromptTemplate.from_template(base_prompt)

    llm = OllamaLLM(model="llama3", streaming=True)
    output_parser = StrOutputParser()

    rag_chain = (
        {
            "context": hybrid_retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
            "question": RunnablePassthrough(),
            "memory": lambda x: formatted_memory
        }
        | prompt
        | llm
        | output_parser
    )
    
    return rag_chain
    