"""File management API endpoints."""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.class_ import Class
from app.models.file import File
from app.schemas.file import FileResponse
from app.utils.dependencies import get_current_user
from app.config import settings
from app.services.transcription_service import transcription_service
from app.services.pdf_service import pdf_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/files", tags=["files"])


def check_class_access(class_id: int, current_user: User, db: Session) -> Class:
    """Check if user has access to a class."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
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

    return class_


@router.get("/class/{class_id}", response_model=List[FileResponse])
async def list_files(
    class_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all files in a class."""
    class_ = check_class_access(class_id, current_user, db)
    return class_.files


@router.post("/class/{class_id}/upload", response_model=FileResponse)
async def upload_file(
    class_id: int,
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file to a class."""
    class_ = check_class_access(class_id, current_user, db)

    # Check file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension in ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma']:
        file_type = 'audio'
    elif file_extension == '.pdf':
        file_type = 'pdf'
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_extension}"
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_size = 0
    with open(file_path, "wb") as f:
        content = await file.read()
        file_size = len(content)
        f.write(content)

    # Create database record
    db_file = File(
        class_id=class_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        is_processed=False
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # Process file in background (transcribe or extract text)
    try:
        if file_type == 'audio':
            # Transcribe audio
            text, transcription_path = transcription_service.transcribe_audio(file_path)
            db_file.transcription_text = text
            db_file.transcription_path = transcription_path
        elif file_type == 'pdf':
            # Extract text from PDF
            text = pdf_service.extract_text(file_path)
            db_file.transcription_text = text

        # Add to RAG system
        rag_service.add_documents(
            class_id=class_id,
            texts=[db_file.transcription_text],
            metadatas=[{"filename": file.filename, "file_id": db_file.id}]
        )

        db_file.is_processed = True
        db.commit()
        db.refresh(db_file)

    except Exception as e:
        print(f"Error processing file: {e}")
        # File is saved but not processed
        db.commit()

    return db_file


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a file."""
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Check access
    check_class_access(file.class_id, current_user, db)

    # Delete physical file
    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    # Delete transcription file
    if file.transcription_path and os.path.exists(file.transcription_path):
        os.remove(file.transcription_path)

    # Remove from RAG system
    try:
        rag_service.remove_documents(file.class_id, file.original_filename)
    except Exception as e:
        print(f"Error removing from RAG: {e}")

    # Delete database record
    db.delete(file)
    db.commit()

    return {"message": "File deleted successfully"}
