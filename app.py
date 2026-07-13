from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback
import time

from config import (
    APP_NAME,
    VERSION,
    HOST,
    PORT,
    ALLOW_ORIGINS,
    MEDIA_TYPE,
    DEFAULT_VOICE,
    DEFAULT_RATE,
    DEFAULT_PITCH,
    DEFAULT_VOLUME
)

from logger import logger
from services.edge import (
    get_voice_list,
    stream_audio
)


# =====================================
# FastAPI
# =====================================

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================
# Request Model
# =====================================

class TTSRequest(BaseModel):

    text: str

    voice: str = DEFAULT_VOICE

    rate: str = DEFAULT_RATE

    pitch: str = DEFAULT_PITCH

    volume: str = DEFAULT_VOLUME


# =====================================
# Runtime Stats
# =====================================

start_time = time.time()

request_count = 0


# =====================================
# Routes
# =====================================

@app.get("/")
def root():

    return {

        "service": APP_NAME,

        "version": VERSION,

        "status": "running"

    }


@app.get("/health")
def health():

    return {

        "status": "ok"

    }


@app.get("/stats")
def stats():

    uptime = int(
        time.time() - start_time
    )

    return {

        "uptime": uptime,

        "requests": request_count

    }


@app.get("/voices")
async def voices():

    return await get_voice_list()


@app.post("/tts")
async def tts(req: TTSRequest):

    global request_count

    request_count += 1

    logger.info("Text Length: %d", len(req.text))

    try:

        return StreamingResponse(

            stream_audio(req),

            media_type=MEDIA_TYPE,

            headers={

                "Cache-Control": "no-cache",

                "Accept-Ranges": "none",

                "X-Accel-Buffering": "no"

            }

        )

    except Exception as e:

        logger.exception(e)

        traceback.print_exc()

        return JSONResponse(

            status_code=500,

            content={

                "error": str(e)

            }

        )


# =====================================
# Main
# =====================================

if __name__ == "__main__":

    import uvicorn

    logger.info("%s started.", APP_NAME)

    uvicorn.run(

        app,

        host=HOST,

        port=PORT

    )