"""Chat API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.class_ import Class
from app.schemas.chat import ChatMessage, ChatResponse, SourceDocument
from app.utils.dependencies import get_current_user
from app.services.rag_service import rag_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ask a question about class materials."""
    # Check if class exists and user has access
    class_ = db.query(Class).filter(Class.id == chat_message.class_id).first()
    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if not current_user.is_admin and class_ not in current_user.classes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Query RAG system
    try:
        answer, sources = rag_service.query(chat_message.class_id, chat_message.message)

        # Format sources
        source_docs = [
            SourceDocument(filename=src["filename"], content=src["content"])
            for src in sources
        ]

        return ChatResponse(answer=answer, sources=source_docs)

    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )
