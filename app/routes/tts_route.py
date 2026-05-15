# import os
# import tempfile
# import edge_tts

# from fastapi import APIRouter, HTTPException, BackgroundTasks
# from fastapi.responses import FileResponse
# from pydantic import BaseModel

# router = APIRouter()


# class TTSRequest(BaseModel):
#     text: str
#     voice: str = "en-US-EricNeural"
#     pitch: str = "-15Hz"
#     rate: str = "-10%"


# async def text_to_speech(text, output_file, voice, pitch, rate):
#     communicate = edge_tts.Communicate(
#         text=text,
#         voice=voice,
#         pitch=pitch,
#         rate=rate
#     )
#     await communicate.save(output_file)


# def cleanup_file(path: str):
#     if os.path.exists(path):
#         os.remove(path)


# @router.post("/tts")
# async def generate_tts(request: TTSRequest, background_tasks: BackgroundTasks):

#     if not request.text.strip():
#         raise HTTPException(status_code=400, detail="Text cannot be empty")

#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#     output_path = temp_file.name
#     temp_file.close()

#     try:
#         await text_to_speech(
#             text=request.text,
#             output_file=output_path,
#             voice=request.voice,
#             pitch=request.pitch,
#             rate=request.rate
#         )

#         # ✅ delete AFTER response is sent
#         background_tasks.add_task(cleanup_file, output_path)

#         return FileResponse(
#             path=output_path,
#             media_type="audio/mpeg",
#             filename="speech.mp3"
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

import edge_tts
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-EricNeural"
    pitch: str = "-15Hz"
    rate: str = "-10%"


@router.post("/tts")
async def generate_tts(request: TTSRequest):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        communicate = edge_tts.Communicate(
            text=request.text,
            voice=request.voice,
            pitch=request.pitch,
            rate=request.rate
        )

        audio_stream = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])

        audio_stream.seek(0)

        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))