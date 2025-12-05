def comparePrices(products):
    if not products:
        return []
    
    def parse_price(p):
        return float(p['price'].replace("LKR","").replace(",","").strip())
    
    min_price_product = min(products,key=parse_price)
    max_price_product = max(products,key=parse_price)

    return {
        "lowest": min_price_product,
        "highest": max_price_product
    }