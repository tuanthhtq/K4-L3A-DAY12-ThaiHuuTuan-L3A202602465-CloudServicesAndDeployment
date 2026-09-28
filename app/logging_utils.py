"""CP1 — Structured logging.

`print("user abc hỏi gì đó")` là log cho người đọc. Cloud (Railway, Render,
Cloud Run, Datadog...) đọc log bằng máy: một dòng = một JSON object thì mới
lọc/đếm/cảnh báo được. Đây là khác biệt lớn giữa localhost và production.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def utc_now_iso() -> str:
    """CHO SẴN — thời điểm hiện tại theo ISO-8601, múi giờ UTC."""
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, level: str = "info", **fields) -> str:
    """Write a one-line JSON event to stdout and return the serialized line."""
    event_data = {
        "event": event,
        "level": level.lower(),
        "timestamp": utc_now_iso(),
    }
    event_data.update(fields)

    serialized = json.dumps(event_data, ensure_ascii=False)
    print(serialized, file=sys.stdout)
    return serialized
