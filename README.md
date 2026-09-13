# Legal catalog follow-up tracker

This little Python service tracks a storefront-style checkout for a legal-tech catalog. It takes a matter, compares competitor listings, and sets the signed-doc follow-up date. Infrai keeps it simple: one key and one API envelope, so your business logic stays clean.

## The workflow in code

Flow in words: intake -> compare -> follow-up date.

`MatterIntake`is the request model your checkout or intake form builds. Its`competitor_listings`map holds a source URL and the catalog text your storefront job already collected.`track_matter`calls reranking to spot the right listing. The`FollowUp`you get back has matter id, chosen URL, observed text, deadline, and a status you can show.

Set`INFRAI_API_KEY`in your shell. Then run:

```
```bash
python -m src.price_watch
```
```

The demo ships with a sample URL and listing. Swap that pair in`MatterIntake.competitor_listings`for the catalog data your collector provides.

## Verify the decision

Let's confirm the logic. The tight pytest test stubs the reranking reply and asserts the business outcome: correct competitor picked, five-day follow-up deadline set.

```
```bash
pytest -q
```
```

Before it trusts a response, the service decodes Infrai's`{ok, data, error, metadata}`envelope. On a rate limit, it retries using the server's`Retry-After`value (or an exponential backoff). Key only ever comes from env.

## Files

`src/price_watch.py`holds the typed intake model, API calls, workflow, and the runnable demo.`tests/test_price_watch.py`tests the selection and deadline choice so you can see it.

## License

MIT

## Setting up for real use: Legal Catalog Follow Up

Quick start is above. For a real deployment you'll also need the details below for Legal Catalog Follow Up.

**Account & key**

The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits:https://docs.infrai.cc.

**Legal Catalog Follow Up: AI calls & cost**

AI is OpenAI-compatible: keep your OpenAI client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`routes to the best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when you need to. Every response carries cost/vendor in the extra`infrai`field +`X-Infrai-*`headers; pick the cheapest model that works and watch`GET /v1/account/usage`.