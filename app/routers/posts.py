from fastapi import APIRouter, HTTPException, Depends
from ..db.database import SessionDep
from ..schema.posts import CreatePost, ReadPosts, UpdatePost
from ..models.posts import Posts
from datetime import datetime
from sqlmodel import select
from loguru import logger
from ..utils import outh_2_scheme, verify_token


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create-post", response_model=ReadPosts)
def create_posts(
    create_post: CreatePost, session: SessionDep, token: str = Depends(outh_2_scheme)
):
    user = None
    logger.info("Logger initialized from posts")
    logger.debug(f"token:{token}")
    if token:
        user, is_valid = verify_token(token, session)  # type: ignore

        if is_valid is False:
            raise HTTPException(status_code=400, detail="Invalid token")

    post = Posts(
        user_id=user.id if user else None,
        title=create_post.title,
        body=create_post.body,
        date=datetime.now(),
    )
    logger.info(f"created:post:{post}")
    try:
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    except Exception as e:
        print(f"error:{e}")


@router.get("/get-posts", response_model=list[ReadPosts])
def get_all_posts(session: SessionDep):
    try:
        posts = session.exec(select(Posts)).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-post/{post_id}", response_model=ReadPosts)
def get_post(post_id: int, session: SessionDep):
    if not post_id:
        raise HTTPException(status_code=400, detail="Id not provided")
    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.patch("/update-post/{post_id}", response_model=ReadPosts)
def update_post(
    post_id: int,
    post_update: UpdatePost,
    session: SessionDep,
    token: str = Depends(outh_2_scheme),
):
    if token:
        user, is_valid = verify_token(token, session)  # type: ignore

        if is_valid is False:
            raise HTTPException(status_code=400, detail="Invalid token")

    if not post_id:
        raise HTTPException(status_code=400, detail="Id not provided")

    post = session.get(Posts, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id:
        if token:
            user, is_valid = verify_token(token, session)  # type: ignore

            if is_valid is False:
                raise HTTPException(status_code=400, detail="Invalid token")
            if user.id != post.user_id:
                raise HTTPException(status_code=403, detail="Unauthorized")
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

    for key, value in post_update.model_dump().items():
        if value is not None:
            setattr(post, key, value)

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.delete("/delete-post/{post_id}")
def delete(post_id: int, session: SessionDep, token: str = Depends(outh_2_scheme)):
    post = session.get_one(Posts, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id:
        if token:
            user, is_valid = verify_token(token, session)  # type: ignore

            if is_valid is False:
                raise HTTPException(status_code=400, detail="Invalid token")
            if user.id != post.user_id:
                raise HTTPException(status_code=403, detail="Unauthorized")
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

    session.delete(post)
    session.commit()

    return {"Post deleted"}
