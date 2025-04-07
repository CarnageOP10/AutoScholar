import os
import chromadb
from typing import Type, List, Dict
from uuid import uuid4
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from transformers import pipeline
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
import torch
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB with Hugging Face embeddings
chroma_client = chromadb.PersistentClient(path="chroma_db")
embedding_function = HuggingFaceEmbeddingFunction(
    api_key=os.getenv("HF_API_TOKEN"),
    model_name="sentence-transformers/all-mpnet-base-v2"
)
collection = chroma_client.get_or_create_collection(
    name="research_papers",
    embedding_function=embedding_function
)

# ----------------------------
# Text Processing Tools
# ----------------------------

class SummarizeInput(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_length: int = Field(130, description="Maximum length of summary")
    min_length: int = Field(30, description="Minimum length of summary")

class SummarizeTool(BaseTool):
    """Tool for summarizing text using Hugging Face models"""
    name: str = "Text Summarizer"
    description: str = "Summarizes text using Hugging Face's BART model"
    args_schema: Type[BaseModel] = SummarizeInput

    def _run(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        result = summarizer(text, max_length=max_length, min_length=min_length)
        return result[0]["summary_text"]

# ----------------------------
# Vector Database Tools
# ----------------------------

class AddToDBInput(BaseModel):
    documents: List[Dict[str, str]] = Field(
        ...,
        description="List of documents with 'text' and optional metadata"
    )

class AddToVectorDBTool(BaseTool):
    """Tool for adding documents to ChromaDB"""
    name: str = "Add to VectorDB"
    description: str = "Stores documents in ChromaDB vector database"
    args_schema: Type[BaseModel] = AddToDBInput

    def _run(self, documents: List[Dict[str, str]]) -> str:
        try:
            ids = [str(uuid4()) for _ in documents]
            texts = [doc["text"] for doc in documents]
            metadatas = [{k: v for k, v in doc.items() if k != "text"} for doc in documents]
            
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return f"Successfully added {len(documents)} documents"
        except Exception as e:
            return f"Error adding documents: {str(e)}"

class QueryDBInput(BaseModel):
    query: str = Field(..., description="Search query")
    n_results: int = Field(5, description="Number of results to return")

class QueryVectorDBTool(BaseTool):
    """Tool for querying ChromaDB"""
    name: str = "Query VectorDB"
    description: str = "Retrieves similar documents from ChromaDB"
    args_schema: Type[BaseModel] = QueryDBInput

    def _run(self, query: str, n_results: int = 5) -> List[Dict[str, str]]:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted = []
            for i in range(len(results["ids"][0])):
                formatted.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "score": results["distances"][0][i]
                })
            return formatted
        except Exception as e:
            return f"Error querying database: {str(e)}"

# ----------------------------
# Web Search Tool (Alternative to WebsiteSearchTool)
# ----------------------------

class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    max_results: int = Field(1, description="Maximum results to return")

class WebSearchTool(BaseTool):
    """Alternative web search tool using SerpAPI"""
    name: str = "Web Search"
    description: str = "Searches the web using SerpAPI only for 1 research paper"
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 1) -> List[Dict[str, str]]:
        try:
            params = {
                "q": query,
                "api_key": os.getenv("SERPAPI_KEY"),
                "num": max_results
            }
            response = requests.get("https://serpapi.com/search", params=params)
            results = response.json().get("organic_results", [])
            
            simplified = []
            for result in results:
                simplified.append({
                    "title": result.get("title"),
                    "url": result.get("link"),
                    "snippet": result.get("snippet")
                })
            return simplified
        except Exception as e:
            return f"Search failed: {str(e)}"