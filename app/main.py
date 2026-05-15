# from fastapi import FastAPI
# from app.routes.tts_route import router as tts_router

# app = FastAPI(
#     title="FastAPI Edge TTS API"
# )

# app.include_router(tts_router)

# @app.get("/")
# def home():
#     return {"message": "TTS API is running"}

# ########################################################################
# from fastapi import FastAPI
# from app.routes.tts_route import router as tts_router

# app = FastAPI()

# app.include_router(tts_router)

# @app.get("/")
# def home():
#     return {"message": "TTS API running on Vercel"}

from fastapi import FastAPI
from app.routes.tts_route import router as tts_router

app = FastAPI()

app.include_router(tts_router)

@app.get("/")
def home():
    return {"message": "TTS API running"}