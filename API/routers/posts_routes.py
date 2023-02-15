"""
Routes for posts
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm.session import Session
from datetime import datetime
import shutil

from schemas.post_schema import PostRequest
from database.database import get_db
from controllers import post_controller

router = APIRouter(
    prefix='/post',
    tags=['posts'],
)

@router.post('/create')
def create_a_post(request: PostRequest, db: Session = Depends(get_db)):
    new_post = post_controller.create_post(db, request)
    return new_post

@router.get('/all')
def get_all_posts(db: Session = Depends(get_db)):
    posts = post_controller.get_posts(db)
    return posts

@router.delete('/{id}')
def delete_a_post(id: int, db: Session = Depends(get_db)):
    return post_controller.delete_post(id, db)

@router.post('/image')
def upload_an_image(image: UploadFile = File(...)):
    file_prefix = str(datetime.utcnow().microsecond) + '.'
    filename = file_prefix.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        'location': path
    }