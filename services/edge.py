import edge_tts

from config import (
    DEFAULT_RATE,
    DEFAULT_PITCH,
    DEFAULT_VOLUME,
    VOICE_CACHE_FILE,
    VOICE_CACHE_EXPIRE
)

from utils import (
    fix_param,
    load_json,
    save_json,
    cache_expired
)

from logger import logger


async def get_voice_list():
    """
    获取中文语音列表
    """

    if (
        not cache_expired(
            VOICE_CACHE_FILE,
            VOICE_CACHE_EXPIRE
        )
    ):

        cache = load_json(
            VOICE_CACHE_FILE
        )

        if cache:
            logger.info("Voice cache hit")
            return cache

    logger.info("Downloading voice list...")

    voices = await edge_tts.list_voices()

    result = []

    for v in voices:

        locale = v["Locale"].lower()

        if "zh" not in locale:
            continue

        result.append({

            "name": v["ShortName"],

            "gender": v["Gender"],

            "locale": v["Locale"]

        })

    save_json(
        VOICE_CACHE_FILE,
        result
    )

    logger.info(
        "Voice count: %d",
        len(result)
    )

    return result


async def stream_audio(req):
    """
    Edge Streaming Generator
    """

    rate = fix_param(
        req.rate,
        DEFAULT_RATE
    )

    pitch = fix_param(
        req.pitch,
        DEFAULT_PITCH
    )

    volume = fix_param(
        req.volume,
        DEFAULT_VOLUME
    )

    logger.info(
        "Voice=%s Rate=%s Pitch=%s Volume=%s",
        req.voice,
        rate,
        pitch,
        volume
    )

    communicate = edge_tts.Communicate(

        text=req.text,

        voice=req.voice,

        rate=rate,

        pitch=pitch,

        volume=volume

    )

    first_chunk = True

    async for chunk in communicate.stream():

        if chunk["type"] != "audio":
            continue

        if first_chunk:
            logger.info("First audio chunk arrived")
            first_chunk = False

        yield chunk["data"]
