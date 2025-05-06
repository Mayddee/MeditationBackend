# import uuid
# from datetime import datetime, timedelta
#
# from fastapi import APIRouter, HTTPException
# from sqlalchemy import select
#
# from src.ORMmodels import User, SharedThought
# from src.database import SessionDep
# from src.pydanticSchemas import ThoughtOut, ThoughtCreate
#
# router = APIRouter()
#
# @router.post("/thoughts/{user_id}", response_model=ThoughtOut)
# async def create_thought(user_id: str, data: ThoughtCreate, session: SessionDep):
#     thought = SharedThought(
#         id=str(uuid.uuid4()),
#         user_id=user_id,
#         content=data.content,
#         image_url=data.image_url,
#         meditation_id=data.meditation_id,
#         created_at=datetime.utcnow(),
#         expires_at=datetime.utcnow() + timedelta(hours=24)
#     )
#     session.add(thought)
#     await session.commit()
#     await session.refresh(thought)
#     return thought
#
# @router.get("/thoughts/", response_model=list[ThoughtOut])
# async def get_public_thoughts(session: SessionDep):
#     result = await session.execute(
#         select(SharedThought).where(SharedThought.expires_at > datetime.utcnow())
#     )
#     return result.scalars().all()
#
# @router.delete("/thoughts/{thought_id}/{user_id}")
# async def delete_thought(thought_id: str, user_id: str, session: SessionDep):
#     thought = await session.get(SharedThought, thought_id)
#     if not thought or thought.user_id != user_id:
#         raise HTTPException(status_code=403)
#     await session.delete(thought)
#     await session.commit()
#     return {"status": "deleted"}