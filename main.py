import binance_history as bh
import ccxt 
import os



def main():
    symbols = bh.fetch_all_symbols(asset_type = "futures/um")
    for s, i in symbols.items():
        if i.type == "future":
            print(s, i)
    
    
    
if __name__ == '__main__':
    main()
