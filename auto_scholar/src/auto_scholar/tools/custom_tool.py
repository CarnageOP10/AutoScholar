from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Type
import uuid

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="research_papers",
    embedding_function=sentence_transformer_ef
)

class SummarizeTextTool(BaseTool):
    """Tool to summarize text using LLM."""
    name = "Summarize Text"
    description = "Summarizes the provided text using an LLM. Returns a concise summary."
    
    def _run(self, text: str) -> str:
        # In a real implementation, you'd call an LLM here
        # This is a simplified version
        sentences = text.split('. ')
        return '. '.join(sentences[:3]) + '...' if len(sentences) > 3 else text

class AddToVectorDBTool(BaseTool):
    """Tool to add text to ChromaDB vector database."""
    name = "Add to VectorDB"
    description = "Adds text documents to ChromaDB vector database with metadata."
    
    def _run(self, documents: List[Dict[str, str]]) -> str:
        """
        Args:
            documents: List of dicts with 'text', 'title', 'source', etc.
        """
        try:
            ids = [str(uuid.uuid4()) for _ in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [{k: v for k, v in doc.items() if k != 'text'} for doc in documents]
            
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return f"Successfully added {len(documents)} documents to ChromaDB"
        except Exception as e:
            return f"Error adding to ChromaDB: {str(e)}"

class GetFromVectorDBTool(BaseTool):
    """Tool to query ChromaDB vector database."""
    name = "Query VectorDB"
    description = "Queries ChromaDB for similar documents based on input query."
    
    def _run(self, query: str, n_results: int = 5) -> List[Dict[str, str]]:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results for the agent
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            return str(formatted_results)
        except Exception as e:
            return f"Error querying ChromaDB: {str(e)}"


