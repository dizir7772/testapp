from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.comments import create_comment, update_comment, delete_comment
from src.schemas.comment_schemas import CommentSchema, CommentsResponse
from src.database.db import get_db
from src.entity.models import User
from src.services.auth_service import get_current_user

router = APIRouter(prefix="/comments", tags=['Comments'])


# Роут для створення коментарів
@router.post("/", response_model=CommentsResponse, status_code=status.HTTP_201_CREATED)
async def create_comments(comment_data: CommentSchema, image_id: int,
                          current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    try:
        created_comment = await create_comment(db, image_id, comment_data.comment, current_user)
        return created_comment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Роут для редагування коментарів
@router.put("/{comment_id}/", response_model=CommentsResponse)
async def update_comments(comment_id: int, comment: CommentSchema,
                          current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    updated_comment = await update_comment(db, comment_id, comment.comment, current_user)

    if updated_comment:
        return updated_comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found or permission denied")


# Роут для видалення коментарів
@router.delete("/{comment_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comments(comment_id: int, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    success = await delete_comment(db, comment_id, current_user)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found or permission denied")