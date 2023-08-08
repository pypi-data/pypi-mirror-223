def stock_price(company):
  if company == "APPL":
    return 100
  elif company == "GOOGL":
    return 130
  elif company == "TSLA":
    return 70
  elif company == "AMZN":
    return 150
  else:
    return 0


funcs_meta = [
    # stock_price()
    {
        "name": "stock_price",
        "description": "Get the stock price of a given company",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "The company stock name, e.g. APPL",
                },
            },
            "required": ["company"],
        },
    }
]

funcs = {
    "stock_price": stock_price
}



