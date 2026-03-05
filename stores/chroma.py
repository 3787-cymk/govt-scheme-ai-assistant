from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from typing import Optional
from langchain_core.documents import Document


def store_embeddings(documents: list[Document], embeddings: GoogleGenerativeAIEmbeddings) -> Optional[Chroma]:
    """
    Store embeddings for the documents using Chroma vectorstore.
    """
    try:
        vectorstore = Chroma.from_documents(
            documents,
            embeddings,
            persist_directory="./chroma_db"
        )

        return vectorstore

    except Exception as e:
        raise Exception(f"Error creating Chroma vectorstore: {e}")


def get_retriever(vectorstore: Chroma) -> VectorStoreRetriever:
    """
    Creates a retriever from Chroma vectorstore with optimized search settings.
    """

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3
        }
    )

    return retriever