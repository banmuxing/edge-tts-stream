# ==========================
# Edge TTS Gateway Config
# ==========================

APP_NAME = "Edge TTS Streaming Gateway"

VERSION = "2.1.0"

HOST = "0.0.0.0"

PORT = 3978


# 默认语音
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

DEFAULT_RATE = "-50%"

DEFAULT_PITCH = "+0Hz"

DEFAULT_VOLUME = "+0%"


# Voice 列表缓存

VOICE_CACHE_FILE = "data/voices.json"

VOICE_CACHE_EXPIRE = 60 * 60 * 24


# Streaming

MEDIA_TYPE = "audio/mpeg"

ALLOW_ORIGINS = ["*"]


# Logging

LOG_LEVEL = "INFO"