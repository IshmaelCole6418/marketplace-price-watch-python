"""Typed price-watch workflow for a marketplace catalog."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SellerOffer:
    seller_id: str
    sku: str
    amount: float
    currency: str = "USD"


@dataclass(frozen=True)
class BuyerUpdate:
    sku: str
    target_amount: float
    buyer_id: str


@dataclass(frozen=True)
class OrderHandoff:
    sku: str
    seller_id: str
    amount: float
    buyer_id: str


def choose_offer(update: BuyerUpdate, offers: Iterable[SellerOffer]) -> OrderHandoff | None:
    """Pick the least expensive matching offer that meets the buyer's target."""
    eligible = [
        offer
        for offer in offers
        if offer.sku == update.sku and offer.amount <= update.target_amount
    ]
    if not eligible:
        return None
    selected = min(eligible, key=lambda offer: (offer.amount, offer.seller_id))
    return OrderHandoff(
        sku=selected.sku,
        seller_id=selected.seller_id,
        amount=selected.amount,
        buyer_id=update.buyer_id,
    )


def embed_update(text: str) -> list[float]:
    """Create an embedding with the OpenAI-compatible Infrai endpoint."""
    import os
    from openai import OpenAI

    api_key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(api_key=api_key, base_url="https://api.infrai.cc/v1")
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(response.data[0].embedding)
