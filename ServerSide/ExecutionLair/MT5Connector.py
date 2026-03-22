# execution/mt5_connector.py
import MetaTrader5 as mt5
from datetime import datetime


class MT5Connector:

    def __init__(self, account, password, server):
        if not mt5.initialize():
            raise RuntimeError(f"MT5 initialization failed: {mt5.last_error()}")
        print("✅ MT5 connected")

        # Login
        authorized = mt5.login(account, password, server)
        if not authorized:
            raise RuntimeError(f"❌ Login failed: {mt5.last_error()}")
        print(f"✅ Logged in to account {account}")


    



    # --------------------------------------------------------------------
    # Send Market Order
    # --------------------------------------------------------------------
    def send_market_order(self, symbol, direction, volume, sl=None, tp=None, magic=12345, comment="bot_trade"):
        mt5.symbol_select(symbol, True)

        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            raise ValueError(f"❌ No tick data for {symbol}")

        price = tick.ask if direction.lower() == "buy" else tick.bid
        order_type = mt5.ORDER_TYPE_BUY if direction.lower() == "buy" else mt5.ORDER_TYPE_SELL

        

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl or 0.0,
            "tp": tp or 0.0,
            "deviation": 20,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Order failed: {result.comment} (code={result.retcode})")
        else:
            print(f"✅ Order executed: {symbol} {direction.upper()} {volume} @ {price}")
            print(f"   SL={sl}  TP={tp}")

        return result


    # --------------------------------------------------------------------
    # Close All Positions
    # --------------------------------------------------------------------
    def close_all_positions(self, symbol=None):
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            print("No positions found.")
            return

        for pos in positions:
            direction = "buy" if pos.type == mt5.ORDER_TYPE_BUY else "sell"
            close_type = mt5.ORDER_TYPE_SELL if direction == "buy" else mt5.ORDER_TYPE_BUY
            tick = mt5.symbol_info_tick(pos.symbol)
            price = tick.bid if direction == "buy" else tick.ask

            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": close_type,
                "position": pos.ticket,
                "price": price,
                "deviation": 20,
                "magic": pos.magic,
                "comment": "close_all",
                "type_time": mt5.ORDER_TIME_GTC,
               
            }

            result = mt5.order_send(close_request)
            print(f"Closed {pos.symbol} -> retcode={result.retcode}")


    # --------------------------------------------------------------------
    # Shutdown
    # --------------------------------------------------------------------
    def shutdown(self):
        mt5.shutdown()