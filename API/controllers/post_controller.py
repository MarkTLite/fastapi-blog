from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from datetime import datetime

from models.post_model import PostModel
from schemas.post_schema import PostRequest
from database.database import get_db


def create_post(db: Session, req: PostRequest):
    """Create and return a new post in the db"""
    new_post = PostModel(
        title=req.title,
        content=req.content,
        image_url=req.image_url,
        creator=req.creator,
        timestamp=datetime.now(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_posts(db: Session):
    """Return all posts"""
    return db.query(PostModel).all()

def delete_post(id: int, db: Session):
    """Delete only when in db"""
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
            )
    db.delete(post)
    db.commit()
    return 'success'

