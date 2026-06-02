# import asyncio
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# import models.DB_model as model
# from vida.database.database import engine
# from apis.router import router as api_router

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# model.Base.metadata.create_all(bind=engine)

# app.include_router(api_router)

# @app.get("/")
# def health():
#     return {"status": "Backend Running"}
