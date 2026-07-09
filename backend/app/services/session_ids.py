import time
import uuid


def generate_call_id() -> str:
    timestamp = int(time.time())
    unique = uuid.uuid4().hex[:12]
    return f"session_{timestamp}_{unique}"
