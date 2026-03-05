from langchain_community.document_loaders import WebBaseLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import Iterable, List
import json


def load_documents(website: str) -> list[Document]:
    """
    Loads documents from a given website.

    Args:
        website (str): The URL of the website to load documents from.

    Returns:
        list[Document]: A list of loaded documents.
    """
    loader = WebBaseLoader(website)
    return loader.load()


def format_documents(docs: list[Document]) -> str:
    """
    Formats a list of documents into a single string.

    Args:
        docs (list[Document]): The list of documents to format.

    Returns:
        str: The formatted documents as a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def split_documents(documents: Iterable[Document]) -> list[Document]:
    """
    Splits documents into smaller chunks for better retrieval accuracy.
    """

    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=350,
    chunk_overlap=60,
    separators=["\n\n", "\n", ".", " ", ""]
)

    return text_splitter.split_documents(documents)

def load_json_to_langchain_document_schema(file_path: str) -> List[Document]:

    docs = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for scheme in data:

        content = f"""
Scheme Name: {scheme.get('name','')}

Category: {scheme.get('category','')}

Description:
{scheme.get('description','')}

Eligibility:
{scheme.get('eligibility','')}

Benefits:
{scheme.get('benefits','')}
"""

        docs.append(
            Document(
                page_content=content,
                metadata={
                    "scheme_name": scheme.get("name",""),
                    "category": scheme.get("category","")
                }
            )
        )

    return docs