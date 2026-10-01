import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from price_watch import BuyerUpdate, SellerOffer, choose_offer


def test_handoff_chooses_lowest_matching_offer() -> None:
    update = BuyerUpdate(sku="coffee-250g", target_amount=12.00, buyer_id="buyer-42")
    offers = [
        SellerOffer("seller-blue", "coffee-250g", 11.95),
        SellerOffer("seller-green", "coffee-250g", 11.90),
        SellerOffer("seller-tea", "tea-100g", 4.00),
        SellerOffer("seller-high", "coffee-250g", 12.50),
    ]

    result = choose_offer(update, offers)

    assert result is not None
    assert result.seller_id == "seller-green"
    assert result.amount == 11.90
    assert result.buyer_id == "buyer-42"
