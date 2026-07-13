import os
import json
import time


def fix_param(value, default):
    """
    修正 Edge 参数格式
    """

    if value is None:
        return default

    value = str(value)

    if value in ("0%", "0Hz"):
        return "+" + value

    if not value.startswith("+") and not value.startswith("-"):
        return "+" + value

    return value


def load_json(path):
    """
    读取 JSON 文件
    """

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return None


def save_json(path, data):
    """
    保存 JSON
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def cache_expired(path, expire_seconds):
    """
    判断缓存是否过期
    """

    if not os.path.exists(path):
        return True

    modify_time = os.path.getmtime(path)

    return (
        time.time() - modify_time
    ) > expire_seconds


def ensure_data_dir(path):
    """
    创建目录
    """

    os.makedirs(path, exist_ok=True)


def now_ms():
    """
    当前毫秒时间
    """

    return int(time.time() * 1000)