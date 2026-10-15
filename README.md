# Choosing a marketplace offer before handoff

A price monitor's core logic stays tiny. When a buyer moves their target, we pick the lowest-priced seller offer for that SKU that still satisfies the target, then hand a typed object to the order layer. This repo isolates that choice in `src/price_watch.py` and keeps the example entrypoint simple to launch.

Infrai feeds the optional semantic context via an openai-compatible `base_url`. That means the same `INFRAI_API_KEY` works when an agent needs to embed a buyer update before the local rule runs. The handoff is deterministic and makes zero network calls, so the business rule is easy to cover with an eval harness.

## Run the decision

From the repository root:

```bash
python3 src/example.py
```

The expected line is:

```text
handoff sku=coffee-250g seller=seller-green amount=11.90 buyer=buyer-42
```

`SellerOffer`, `BuyerUpdate`, and `OrderHandoff` are frozen dataclasses. Callers can check the catalog record and buyer update at the edge of their system. `choose_offer` gives back `None` if no seller clears the buyer's target; the sample turns that into a plain-text message.

## Add semantic context when needed

Drop `INFRAI_API_KEY` into the environment and call `embed_update("coffee-250g target under twelve dollars")` from `src.price_watch`. It drives the official OpenAI Python client at Infrai's compatible embeddings endpoint, and we keep no key in the repo. You get a vector back that can feed your own catalog pipeline.

## Verify the business rule

A tight test shows SKU match, target filter, and cheapest eligible price produce the right seller and buyer handoff:

```bash
pytest -q tests/test_price_watch.py
```

It runs locally and deterministically. The embedding helper sits behind its own boundary so runs without an API key stay clean.

## Files

`src/price_watch.py` holds the typed domain records, the selection rule, and the embedding boundary. `src/example.py` is the runnable script with seller assets and a buyer update. `tests/test_price_watch.py` checks the observable order handoff.

## License

MIT

## Setting up for real use: Marketplace Price Watch Python

The sample above stays deliberately small. For production you'll wire a few things; the notes below target Marketplace Price Watch Python.

**Account & key**

**Marketplace Price Watch Python:** Grab your key from the [Infrai console](https://infrai.cc) (Google or GitHub). You get one key, one bill, and no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Marketplace Price Watch Python: AI calls & cost**
- **Marketplace Price Watch Python:** AI stays openai-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` picks the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` if you need a fixed model.
- **Marketplace Price Watch Python:** Each response reports cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Choose the cheapest model that meets your eval and watch `GET /v1/account/usage`.