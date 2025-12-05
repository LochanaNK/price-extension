def comparePrices(products):
    if not products:
        return {"lowest": None, "highest": None}
    
    def parse_price(p):
        price_str = p.get('price', '').replace("LKR", "").replace("Rs.", "").replace(",", "").strip()
        try:
            return float(price_str)
        except ValueError:
            return float('inf')  # Treat invalid/missing prices as infinitely high
    
    # Filter out products that have no valid numeric price
    valid_products = [p for p in products if parse_price(p) != float('inf')]
    
    if not valid_products:
        return {"lowest": None, "highest": None}
    
    min_price_product = min(valid_products, key=parse_price)
    max_price_product = max(valid_products, key=parse_price)

    return {
        "lowest": min_price_product,
        "highest": max_price_product
    }
