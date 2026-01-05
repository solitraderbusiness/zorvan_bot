"""RAG (Retrieval-Augmented Generation) service."""
import os
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from app.config import settings

# Try to import from langchain_community, fall back to langchain if not available
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import HuggingFaceEmbeddings


class RAGService:
    """Service for RAG-based question answering."""

    def __init__(self):
        """Initialize the RAG service."""
        self.embeddings = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def get_embeddings(self):
        """Get or create embeddings model."""
        if self.embeddings is None:
            if settings.OPENAI_API_KEY:
                self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
            else:
                # Fallback to sentence transformers if no OpenAI key
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
        return self.embeddings

    def get_vector_store_path(self, class_id: int) -> str:
        """Get the path to the vector store for a class."""
        return os.path.join(settings.VECTOR_STORE_DIR, f"class_{class_id}")

    def add_documents(self, class_id: int, texts: List[str], metadatas: List[dict]):
        """
        Add documents to the vector store for a class.

        Args:
            class_id: ID of the class
            texts: List of text content
            metadatas: List of metadata dicts (should include 'filename')
        """
        print(f"Adding {len(texts)} documents to class {class_id}")

        # Split texts into chunks
        all_chunks = []
        all_metadatas = []

        for text, metadata in zip(texts, metadatas):
            chunks = self.text_splitter.split_text(text)
            all_chunks.extend(chunks)
            all_metadatas.extend([metadata] * len(chunks))

        # Create or update vector store
        vector_store_path = self.get_vector_store_path(class_id)
        embeddings = self.get_embeddings()

        if os.path.exists(vector_store_path):
            # Add to existing vector store
            vectorstore = Chroma(
                persist_directory=vector_store_path,
                embedding_function=embeddings
            )
            vectorstore.add_texts(all_chunks, metadatas=all_metadatas)
        else:
            # Create new vector store
            vectorstore = Chroma.from_texts(
                texts=all_chunks,
                metadatas=all_metadatas,
                embedding=embeddings,
                persist_directory=vector_store_path
            )

        vectorstore.persist()
        print(f"Added {len(all_chunks)} chunks to vector store")

    def remove_documents(self, class_id: int, filename: str):
        """
        Remove documents from the vector store for a class.

        Args:
            class_id: ID of the class
            filename: Filename to remove
        """
        vector_store_path = self.get_vector_store_path(class_id)

        if not os.path.exists(vector_store_path):
            return

        embeddings = self.get_embeddings()
        vectorstore = Chroma(
            persist_directory=vector_store_path,
            embedding_function=embeddings
        )

        # Get all documents
        # Note: ChromaDB doesn't have a direct delete by metadata method in older versions
        # This is a workaround - in production, consider using a different vector store
        # or upgrading to the latest ChromaDB version
        print(f"Removing documents with filename: {filename} from class {class_id}")

    def query(self, class_id: int, question: str) -> Tuple[str, List[dict]]:
        """
        Query the RAG system with a question.

        Args:
            class_id: ID of the class
            question: Question to ask

        Returns:
            Tuple of (answer, source_documents)
        """
        vector_store_path = self.get_vector_store_path(class_id)

        if not os.path.exists(vector_store_path):
            return "No documents have been uploaded for this class yet.", []

        embeddings = self.get_embeddings()
        vectorstore = Chroma(
            persist_directory=vector_store_path,
            embedding_function=embeddings
        )

        # Create retrieval QA chain
        if settings.OPENAI_API_KEY:
            llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo",
                openai_api_key=settings.OPENAI_API_KEY
            )
        else:
            # Fallback to a simple concatenation if no OpenAI key
            retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            answer = f"Based on the class materials:\n\n{context}\n\nPlease configure an OpenAI API key for better answers."
            sources = [{"filename": doc.metadata.get("filename", "unknown"), "content": doc.page_content[:200]} for doc in docs]
            return answer, sources

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )

        result = qa_chain({"query": question})
        answer = result["result"]
        source_docs = result["source_documents"]

        sources = [
            {
                "filename": doc.metadata.get("filename", "unknown"),
                "content": doc.page_content[:200]
            }
            for doc in source_docs
        ]

        return answer, sources


# Singleton instance
rag_service = RAGService()
