# Context

A staff engineer preparing a design review asks for an ownership audit
before greenlighting a new "price-matched" promo type for a second
product line:

> I want to make sure we understand who owns `final_price` and the
> price-match discount before we extend this pattern further. Can you
> audit ownership here?

Files in this directory (`pricing.py`, `promotions.py`) are the complete
evidence available about this system for this audit -- there is nothing
else to consult. `product_id` for a price-matched promo's
`competitor_product_id` always refers to a different product than the one
the promo applies to (never itself).
