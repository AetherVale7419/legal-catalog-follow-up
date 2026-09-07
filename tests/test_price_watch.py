from datetime import date

from src.price_watch import FollowUp, MatterIntake, track_matter


def test_matter_uses_matching_competitor_and_sets_deadline(monkeypatch):
    calls = []

    def fake_post(path, payload):
        calls.append((path, payload))
        return {"results": [{"text": "$500"}]}

    monkeypatch.setattr("src.price_watch._post", fake_post)
    result = track_matter(MatterIntake("m-1", "contract review", {"https://example.com/legal/contract-review": "$500"}, "signed.pdf", 5))
    assert isinstance(result, FollowUp)
    assert result.selected_url.endswith("contract-review")
    assert result.deliver_by >= date.today()
    assert [path for path, _ in calls] == ["/v1/ai/rerank"]
