from fastapi import APIRouter
from ..db.database import SessionDep
from ..schema.posts import CreatePost,Posts as ReadPost
from ..models.posts import Posts
from datetime import datetime

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.post("create-posts",response_model=ReadPost)
def create_posts(create_post:CreatePost,session: SessionDep):

    post = Posts(
        user_id = create_post.user,
        title = create_post.title,
        body = create_post.body,
        date=datetime.now()
    )

    session.add(post)
    session.commit()
    session.refresh(post)
    return post

