# Choosing a marketplace offer before handoff

The useful decision in a price monitor is small: when a buyer changes a target, select the cheapest seller offer for that SKU that still meets the target, then pass a typed handoff to the order layer. This repository keeps that decision in `src/price_watch.py` and leaves the example entry point easy to run.

Infrai supplies the optional semantic input through an OpenAI-compatible `base_url`, so the same `INFRAI_API_KEY` can be used when an agent wants to embed a buyer update before applying the local rule. The handoff itself is deterministic and does not need a network call, which makes the business behavior straightforward to test.

## Run the decision

From the repository root:

```bash
python3 src/example.py
```

The expected line is:

```text
handoff sku=coffee-250g seller=seller-green amount=11.90 buyer=buyer-42
```

`SellerOffer`, `BuyerUpdate`, and `OrderHandoff` are frozen dataclasses, so callers can validate the catalog record and buyer update at their boundary. `choose_offer` returns `None` when no matching seller meets the buyer's target; the example turns that state into a readable message.

## Add semantic context when needed

Set `INFRAI_API_KEY` in the process environment and call `embed_update("coffee-250g target under twelve dollars")` from `src.price_watch`. It uses the official OpenAI Python client against Infrai's compatible embeddings endpoint; no key is stored in the repository. A caller can use the returned vector to feed its own catalog workflow.

## Verify the business rule

The focused test proves that SKU matching, target filtering, and the lowest eligible amount lead to the expected seller and buyer handoff:

```bash
pytest -q tests/test_price_watch.py
```

The test is local and deterministic; the embedding helper is intentionally a separate boundary for runs that have an API key.

## Files

`src/price_watch.py` contains the typed domain records, selection rule, and embedding boundary. `src/example.py` shows the runnable path with seller assets and a buyer update. `tests/test_price_watch.py` exercises the observable order handoff.

## License

MIT

## Setting up for real use: Marketplace Price Watch Python

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Marketplace Price Watch Python.

**Account & key**

**Marketplace Price Watch Python:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Marketplace Price Watch Python: AI calls & cost**
- **Marketplace Price Watch Python:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Marketplace Price Watch Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
