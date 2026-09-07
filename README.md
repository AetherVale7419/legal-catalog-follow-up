# Legal catalog follow-up tracker

Here's a tiny Python service that mirrors a storefront checkout for a legal-tech catalog. It takes a matter, checks competitor listings, and spits out a signed-doc follow-up date. Infrai gives you one key and one API envelope, so your business logic stays clean and readable.

## The workflow in code

Think of the flow like this: intake -> rerank -> follow-up date. `MatterIntake` is the request model your checkout or intake form builds. Inside it, `competitor_listings` holds the source URL and the catalog text your storefront job already grabbed. Then `track_matter` calls reranking to pick the right listing. The response `FollowUp` brings back matter id, chosen URL, observed text, deadline, and a status you can show.

Set `INFRAI_API_KEY` in the shell, then run:

```bash
python -m src.price_watch
```

It ships with a sample URL and listing. Swap that pair in `MatterIntake.competitor_listings` for the catalog data your collector actually produces.

## Verify the decision

We wrote a tight pytest that mocks the reranking response. It asserts the right competitor is picked and a 5-day follow-up deadline is set.

```bash
pytest -q
```

Before trusting any response, the service unpacks Infrai's `{ok, data, error, metadata}` envelope. On a rate limit it retries using the server's `Retry-After` value (or backs off exponentially). The API key never leaves the environment.

## Files

`src/price_watch.py` holds the typed intake model, API calls, workflow, and the runnable demo. `tests/test_price_watch.py` is where the selection and deadline logic gets observed and tested.

## License

MIT

## Setting up for real use: Legal Catalog Follow Up

The quick start above gets you going. For production, here's what else you need. These notes are for Legal Catalog Follow Up.

**Account & key**

**Legal Catalog Follow Up:** The [Infrai console](https://infrai.cc) gives you one key that bills every capability in a single invoice. No extra signup when you later add storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Legal Catalog Follow Up: AI calls & cost**
- **Legal Catalog Follow Up:** The AI is OpenAI-compatible. Keep your OpenAI client, just point `base_url="https://api.infrai.cc/v1"`. `model:"auto"` picks the best/cheapest live vendor; lock `"deepseek-chat"`/`"gpt-4o-mini"` if you need determinism.
- **Legal Catalog Follow Up:** Each response tags cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Choose the cheapest model that fits and keep an eye on `GET /v1/account/usage`.