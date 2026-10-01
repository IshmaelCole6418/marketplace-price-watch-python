"""Runnable example: inspect offers, then prepare an order handoff."""

import os

from price_watch import BuyerUpdate, SellerOffer, choose_offer, embed_update


def main() -> None:
    if os.getenv("INFRAI_API_KEY"):
        embed_update("coffee-250g target under twelve dollars")

    offers = [
        SellerOffer(seller_id="seller-blue", sku="coffee-250g", amount=12.50),
        SellerOffer(seller_id="seller-green", sku="coffee-250g", amount=11.90),
        SellerOffer(seller_id="seller-red", sku="tea-100g", amount=6.00),
    ]
    update = BuyerUpdate(sku="coffee-250g", target_amount=12.00, buyer_id="buyer-42")
    handoff = choose_offer(update, offers)
    if handoff is None:
        print("No offer meets the buyer's target.")
        return
    print(f"handoff sku={handoff.sku} seller={handoff.seller_id} amount={handoff.amount:.2f} buyer={handoff.buyer_id}")


if __name__ == "__main__":
    main()
