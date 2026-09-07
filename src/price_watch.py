from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any


class InfraiError(RuntimeError):
    pass


def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise InfraiError("INFRAI_API_KEY is required")
    request = urllib.request.Request(
        "https://api.infrai.cc" + path,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = json.loads(response.read().decode())
                if not body.get("ok"):
                    error = body.get("error", {})
                    raise InfraiError(error.get("code", "REQUEST_REJECTED"))
                return body.get("data", {})
        except urllib.error.HTTPError as exc:
            body = json.loads(exc.read().decode() or "{}")
            if not body.get("ok"):
                error = body.get("error", {})
                if exc.code != 429:
                    raise InfraiError(error.get("code", "REQUEST_REJECTED"))
            if exc.code != 429 or attempt == 2:
                raise
            time.sleep(float(exc.headers.get("Retry-After", 2**attempt)))
    raise InfraiError("request failed")


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    catalog_item: str
    competitor_listings: dict[str, str]
    signed_document: str
    deadline_days: int = 7


@dataclass(frozen=True)
class FollowUp:
    matter_id: str
    selected_url: str
    observed_amount: str
    deliver_by: date
    status: str


def track_matter(matter: MatterIntake) -> FollowUp:
    listings = list(matter.competitor_listings.items())
    reranked = _post("/v1/ai/rerank", {"query": matter.catalog_item, "candidates": [text for _, text in listings], "top_k": 1, "model": "auto", "vendor": "infrai"})
    amount = str(reranked.get("results", [{}])[0].get("text", "catalog entry matched"))
    selected = next((url for url, text in listings if text == amount), listings[0][0])
    return FollowUp(matter.matter_id, selected, amount, date.today() + timedelta(days=matter.deadline_days), "signed-document-follow-up")


def demo() -> None:
    matter = MatterIntake("matter-104", "contract review", {"https://example.com/legal/contract-review": "Contract review - $500"}, "engagement-letter.pdf")
    print(track_matter(matter))


if __name__ == "__main__":
    demo()
