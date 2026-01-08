from typing import List
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate

from build_vectore import get_vector_store
from retriever import create_retriever
from llm import create_chat


class State(MessagesState):
    documents: List[str]


def retrieve_documents(state: State) -> State:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004"
    )
    vector_store = get_vector_store(embeddings)
    retriever = create_retriever(vector_store)

    query = state["messages"][-1].content
    docs = retriever.invoke(query)

    document_pages = [doc.page_content for doc in docs]

    return {"documents": document_pages}


def generate_answer(state: State) -> State:
    chat = create_chat()

    documents = "\n\n".join(state["documents"])
    question = state["messages"][-1].content

    prompt_template = PromptTemplate(
        input_variables=["documents", "question"],
        template="""
Use ONLY the following documents to answer the question.

Documents:
{documents}

Question:
{question}

If the answer is not found in the documents, respond with:
"I don't know."
"""
    )

    prompt = prompt_template.format(
        documents=documents,
        question=question
    )

    response = chat.invoke(prompt)

    return {"messages": state['messages'] + [response]}


def build_graph():
    graph = StateGraph(State)

    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()
