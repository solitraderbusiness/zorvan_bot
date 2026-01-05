"""Class management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.class_ import Class
from app.schemas.class_ import ClassCreate, ClassResponse
from app.utils.dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("/", response_model=List[ClassResponse])
async def list_classes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all classes the user has access to."""
    if current_user.is_admin:
        # Admins can see all classes
        classes = db.query(Class).all()
    else:
        # Regular users can only see their assigned classes
        classes = current_user.classes

    # Add file count to each class
    result = []
    for class_ in classes:
        class_dict = ClassResponse.from_orm(class_).dict()
        class_dict["file_count"] = len(class_.files)
        result.append(ClassResponse(**class_dict))

    return result


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(
    class_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific class."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    # Check access
    if not current_user.is_admin and class_ not in current_user.classes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    class_dict = ClassResponse.from_orm(class_).dict()
    class_dict["file_count"] = len(class_.files)
    return ClassResponse(**class_dict)


@router.post("/", response_model=ClassResponse)
async def create_class(
    class_create: ClassCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new class (admin only)."""
    db_class = Class(
        name=class_create.name,
        description=class_create.description
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)

    class_dict = ClassResponse.from_orm(db_class).dict()
    class_dict["file_count"] = 0
    return ClassResponse(**class_dict)


@router.put("/{class_id}", response_model=ClassResponse)
async def update_class(
    class_id: int,
    class_update: ClassCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a class (admin only)."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    class_.name = class_update.name
    class_.description = class_update.description

    db.commit()
    db.refresh(class_)

    class_dict = ClassResponse.from_orm(class_).dict()
    class_dict["file_count"] = len(class_.files)
    return ClassResponse(**class_dict)


@router.delete("/{class_id}")
async def delete_class(
    class_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a class (admin only)."""
    import shutil
    from app.services.rag_service import rag_service

    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    # Delete vector store
    vector_store_path = rag_service.get_vector_store_path(class_id)
    if os.path.exists(vector_store_path):
        shutil.rmtree(vector_store_path)

    # Delete class (files will be cascade deleted)
    db.delete(class_)
    db.commit()

    return {"message": "Class deleted successfully"}


import os
