import cbpro
import math
import time


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

API_KEY = input('API KEY:')
API_SECRET = input('API SECRET:')
API_PASSWORD = input('API PASSPHRASE:')

client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASSWORD)
count = 0
while count < 99999:
    balances = client.get_accounts()

    for b in balances:
        if b['currency'] != 'USD':
            sell_asset = str(b['currency'])
            balance = float(b['balance'])
            symbol = str(sell_asset + 'USD')
            price = float(client.get_product_ticker(symbol)['price'])
            value = balance * price
            if value >= 10:
                currencies = client.get_products()
                for c in currencies:
                    if c['id'] == symbol:
                        minimum = float(c['base_min_size'])
                if minimum <= .001:
                    sell_asset = truncate(sell_asset, 4)
                else:
                    if minimum <= .01:
                        sell_asset = truncate(sell_asset, 3)
                    else:
                        if minimum <= .1:
                            sell_asset = truncate(sell_asset, 2)
                        else:
                            if minimum <= 1:
                                sell_asset = truncate(sell_asset, 1)
                            else:
                                if minimum == 1:
                                    sell_asset = int(sell_asset)
                client.place_market_order(product_id=symbol, side='sell', size=balance)
    count = count + 1
    time.sleep(60)

# If you feel like donating, send ETH or USDC to : 0x3f60008Dfd0EfC03F476D9B489D6C5B13B3eBF2C
#            And make sure to check out our open source rebalancing software in its upcoming release!