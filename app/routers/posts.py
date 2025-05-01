from fastapi import APIRouter,HTTPException
from ..db.database import SessionDep
from ..schema.posts import CreatePost,ReadPosts,UpdatePost
from ..models.posts import Posts
from datetime import datetime
from sqlmodel import select
from ..models.user import User
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Optional, for safety
logger.debug("posts logger initialized")

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.post("/create-posts",response_model=ReadPosts)
def create_posts(create_post:CreatePost,session: SessionDep):
    user = None
    if create_post.user:
        statement = select(User).where(User.id==create_post.user)
        queried_user = session.exec(statement).first()
        if not queried_user:
            raise HTTPException(status_code=400, detail="User not found")
        user = create_post.user


    post = Posts(
        user_id = user,
        title = create_post.title,
        body = create_post.body,
        date=datetime.now()
    )
    try:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    except Exception as e:
        print(f"error:{e}")

@router.get("/get-posts",response_model=list[ReadPosts])
def get_all_posts(session:SessionDep):
    try:
        posts = session.exec(select(Posts)).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get("/get-post/{post_id}",response_model=ReadPosts)
def get_post(post_id:int,session:SessionDep):
    if not post_id :
        raise HTTPException(status_code=400,detail="Id not provided")
    print(f"post_id;{post_id}")
    post = session.get(Posts, post_id)
    print(f"post;{post}")
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")

    return post

@router.patch("/update-post/{post_id}",response_model=ReadPosts)
def update_post(post_id:int,post_update:UpdatePost,session:SessionDep):

    if not post_id :
        raise HTTPException(status_code=400,detail="Id not provided")

    post = session.get(Posts, post_id)

    if not post:
        raise HTTPException(status_code=404,detail="Post not found")

    for key, value in post_update.model_dump().items():
        if value is not None:
            setattr(post,key,value)

    session.add(post)
    session.commit()
    session.refresh(post)

    return post

@router.delete("/delete-post/{post_id}")
def delete(post_id:int,session:SessionDep):
    if not post_id :
        raise HTTPException(status_code=400,detail="Id not provided")

    post = session.get_one(Posts,post_id)

    if not post:
        raise HTTPException(status_code=404,detail="Post not found")


    session.delete(post)
    session.commit()

    return {"Post deleted"}








