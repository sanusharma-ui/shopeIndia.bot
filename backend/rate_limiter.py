import time
from fastapi import HTTPException, Request
from config import settings


VISITORS: dict[str, list[float]] = {}


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


def check_rate_limit(request: Request):
    ip = get_client_ip(request)
    now = time.time()
    window_start = now - 60

    timestamps = VISITORS.get(ip, [])
    timestamps = [timestamp for timestamp in timestamps if timestamp > window_start]

    if len(timestamps) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Too many messages. Please wait for a minute and try again."
        )

    timestamps.append(now)
    VISITORS[ip] = timestamps