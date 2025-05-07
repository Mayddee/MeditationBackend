from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.CRUD.diaries import router as diaries_router
from src.CRUD.users import router as users_router
from src.CRUD.meditations import router as meditations_router
from src.CRUD.sections import router as sections_router
from src.database import router as database_router, Base, engine

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(database_router)
app.include_router(users_router)
app.include_router(diaries_router)
app.include_router(meditations_router)
app.include_router(sections_router)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables created.")






