import base64
import json

def _decode_payload(token: str):
    try:
        parts = token.split(".")
        payload_b64 = parts[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        return json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
    except Exception:
        return None

def get_role_from_jwt(token: str):
    payload = _decode_payload(token)
    return payload.get("role") if payload else None

def get_username_from_jwt(token: str):
    payload = _decode_payload(token)
    return payload.get("sub") if payload else None
